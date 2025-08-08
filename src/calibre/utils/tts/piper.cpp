/*
 * piper.cpp
 * Copyright (C) 2025 Kovid Goyal <kovid at kovidgoyal.net>
 *
 * Distributed under terms of the GPL3 license.
 */
#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <espeak-ng/speak_lib.h>
#include <vector>
#include <map>
#include <memory>
#include <queue>
#include <cstdint>
#include <algorithm>
#include <limits>
#include <chrono>
#ifdef _WIN32
#define ORT_DLL_IMPORT
#endif
#include <onnxruntime_cxx_api.h>

#define CLAUSE_INTONATION_FULL_STOP 0x00000000
#define CLAUSE_INTONATION_COMMA 0x00001000
#define CLAUSE_INTONATION_QUESTION 0x00002000
#define CLAUSE_INTONATION_EXCLAMATION 0x00003000

#define CLAUSE_TYPE_CLAUSE 0x00040000
#define CLAUSE_TYPE_SENTENCE 0x00080000

#define CLAUSE_PERIOD (40 | CLAUSE_INTONATION_FULL_STOP | CLAUSE_TYPE_SENTENCE)
#define CLAUSE_COMMA (20 | CLAUSE_INTONATION_COMMA | CLAUSE_TYPE_CLAUSE)
#define CLAUSE_QUESTION (40 | CLAUSE_INTONATION_QUESTION | CLAUSE_TYPE_SENTENCE)
#define CLAUSE_EXCLAMATION                                                     \
    (45 | CLAUSE_INTONATION_EXCLAMATION | CLAUSE_TYPE_SENTENCE)
#define CLAUSE_COLON (30 | CLAUSE_INTONATION_FULL_STOP | CLAUSE_TYPE_CLAUSE)
#define CLAUSE_SEMICOLON (30 | CLAUSE_INTONATION_COMMA | CLAUSE_TYPE_CLAUSE)
static const bool USE_GPU = false;
static const bool PRINT_TIMING_INFORMATION = false;

typedef char32_t Phoneme;
typedef int64_t PhonemeId;
typedef int64_t SpeakerId;
typedef std::map<Phoneme, std::vector<PhonemeId>> PhonemeIdMap;
const PhonemeId ID_PAD = 0; // interleaved
const PhonemeId ID_BOS = 1; // beginning of sentence
const PhonemeId ID_EOS = 2; // end of sentence

static bool initialized = false, voice_set = false;
PyObject *normalize_func = NULL;
static char espeak_data_dir[512] = {0};
static PhonemeIdMap current_phoneme_id_map;
static int current_sample_rate = 0;
static int current_num_speakers = 1;
static float current_length_scale = 1;
static float current_noise_scale = 1;
static float current_noise_w  = 1;
static float current_sentence_delay  = 0;
static bool current_normalize_volume = true;
std::unique_ptr<Ort::Session> session;
std::queue<std::vector<PhonemeId>> phoneme_id_queue;
std::vector<float> chunk_samples;
static struct {
    PyObject *func, *args;
} normalize_data = {0};

static const std::vector<std::string>& PRIORITY_ORDER = {
#ifdef _WIN32
    "DML", "DmlExecutionProvider", "DirectMLExecutionProvider",
#endif
#ifdef __APPLE__
    "CoreML", "CoreMLExecutionProvider",
#endif
    "ROCMExecutionProvider",  // AMD GPU
    "TensorRTExecutionProvider", "CUDAExecutionProvider", // NVIDIA GPU
    "OpenVINO", "OpenVINOExecutionProvider", // Intel GPU and CPU
    // The various CPU providers
    "DnnlExecutionProvider",  // CPU with AVX 512
    "CPUExecutionProvider",  // the default, always available provider
};

static void
sort_providers_by_priority(std::vector<std::string>& providers, const std::vector<std::string>& priority_order) {
    // Build a priority map: provider name -> order index
    std::unordered_map<std::string, size_t> priority_map;
    for (size_t i = 0; i < priority_order.size(); ++i) {
        priority_map[priority_order[i]] = i;
    }

    // Stable sort so original order is preserved for equal priority
    std::stable_sort(providers.begin(), providers.end(),
        [&priority_map, &priority_order](const std::string& a, const std::string& b) {
            auto it_a = priority_map.find(a);
            auto it_b = priority_map.find(b);
            size_t index_a = it_a != priority_map.end() ? it_a->second : priority_order.size();
            size_t index_b = it_b != priority_map.end() ? it_b->second : priority_order.size();
            return index_a < index_b;
        });
}

static std::vector<std::string> available_providers;

static void
set_available_providers() {
    static bool providers_set = false;
    if (providers_set || !USE_GPU) return;
    providers_set = true;
    Ort::SessionOptions opts;
    opts.DisableCpuMemArena();
    opts.DisableMemPattern();
    opts.DisableProfiling();
    Ort::Env ort_env{ORT_LOGGING_LEVEL_WARNING, "piper"};
    ort_env.DisableTelemetryEvents();

    for (const std::string& s : Ort::GetAvailableProviders()) {
        if (s == "CPUExecutionProvider") continue;
        std::unordered_map<std::string, std::string> provider_options;
        try {
            opts.AppendExecutionProvider(s, provider_options);
            available_providers.push_back(s);
        } catch (const Ort::Exception& e) {
        }
    }
    sort_providers_by_priority(available_providers, PRIORITY_ORDER);
}

static PyObject*
initialize(PyObject *self, PyObject *args) {
    const char *path = "";
    if (!PyArg_ParseTuple(args, "|s", &path)) return NULL;
    if (!initialized || strcmp(espeak_data_dir, path) != 0) {
        if (espeak_Initialize(AUDIO_OUTPUT_SYNCHRONOUS, 0, path && path[0] ? path : NULL, 0) < 0) {
            PyErr_Format(PyExc_ValueError, "Could not initialize espeak-ng with datadir: %s", path ? path : "<default>");
            return NULL;
        }
        Py_CLEAR(normalize_data.func); Py_CLEAR(normalize_data.args);
        initialized = true;
        snprintf(espeak_data_dir, sizeof(espeak_data_dir), "%s", path);
        PyObject *unicodedata = PyImport_ImportModule("unicodedata");
        if (!unicodedata) return NULL;
        normalize_data.func = PyObject_GetAttrString(unicodedata, "normalize");
        Py_CLEAR(unicodedata);
        if (!normalize_data.func) return NULL;
        normalize_data.args = Py_BuildValue("(ss)", "NFD", "");
        if (!normalize_data.args) return NULL;
        set_available_providers();
    }
    Py_RETURN_NONE;
}

static PyObject*
set_espeak_voice_by_name(PyObject *self, PyObject *pyname) {
    if (!PyUnicode_Check(pyname)) { PyErr_SetString(PyExc_TypeError, "espeak voice name must be a unicode string"); return NULL; }
    if (!initialized) { PyErr_SetString(PyExc_Exception, "must call initialize() first"); return NULL; }
    if (espeak_SetVoiceByName(PyUnicode_AsUTF8(pyname)) < 0) {
        PyErr_Format(PyExc_ValueError, "failed to set espeak voice: %U", pyname);
        return NULL;
    }
    voice_set = true;
    Py_RETURN_NONE;
}

static const char*
categorize_terminator(int terminator) {
    const char *terminator_str = "";
    terminator &= 0x000FFFFF;
    switch(terminator) {
        case CLAUSE_PERIOD: terminator_str = "."; break;
        case CLAUSE_QUESTION: terminator_str = "?"; break;
        case CLAUSE_EXCLAMATION: terminator_str = "!"; break;
        case CLAUSE_COMMA: terminator_str = ","; break;
        case CLAUSE_COLON: terminator_str = ":"; break;
        case CLAUSE_SEMICOLON: terminator_str = ";"; break;
    }
    return terminator_str;
}

static PyObject*
phonemize(PyObject *self, PyObject *pytext) {
    if (!PyUnicode_Check(pytext)) { PyErr_SetString(PyExc_TypeError, "text must be a unicode string"); return NULL; }
    if (!initialized) { PyErr_SetString(PyExc_Exception, "must call initialize() first"); return NULL; }
    if (!voice_set) { PyErr_SetString(PyExc_Exception, "must set the espeak voice first"); return NULL; }
    PyObject *phonemes_and_terminators = PyList_New(0);
    if (!phonemes_and_terminators) return NULL;
    const char *text = PyUnicode_AsUTF8(pytext);

    while (text != NULL) {
        int terminator = 0;
        const char *phonemes;
        Py_BEGIN_ALLOW_THREADS;
        phonemes = espeak_TextToPhonemesWithTerminator(
            (const void **)&text, espeakCHARS_UTF8, espeakPHONEMES_IPA, &terminator);
        Py_END_ALLOW_THREADS;
        // Categorize terminator
        const char *terminator_str = categorize_terminator(terminator);
        PyObject *item = Py_BuildValue("(ssO)", phonemes, terminator_str, (terminator & CLAUSE_TYPE_SENTENCE) != 0 ? Py_True : Py_False);
        if (item == NULL) { Py_CLEAR(phonemes_and_terminators); return NULL; }
        int ret = PyList_Append(phonemes_and_terminators, item);
        Py_CLEAR(item);
        if (ret != 0) { Py_CLEAR(phonemes_and_terminators); return NULL; }
    }
    return phonemes_and_terminators;
}

static
long long now() {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

static PyObject*
set_voice(PyObject *self, PyObject *args) {
    PyObject *cfg; PyObject *pymp;
    if (!PyArg_ParseTuple(args, "OU", &cfg, &pymp)) return NULL;

    PyObject *evn = PyObject_GetAttrString(cfg, "espeak_voice_name");
    if (!evn) return NULL;
    PyObject *ret = set_espeak_voice_by_name(NULL, evn);
    Py_CLEAR(evn);
    if (ret == NULL) return NULL;
    Py_DECREF(ret);

#define G(name, dest, conv) { \
        PyObject *sr = PyObject_GetAttrString(cfg, #name); \
        if (!sr) return NULL; \
        dest = conv(sr); Py_CLEAR(sr); \
        if (PyErr_Occurred()) return NULL; \
}
    G(sample_rate, current_sample_rate, PyLong_AsLong);
    G(num_speakers, current_num_speakers, PyLong_AsLong);
    G(length_scale, current_length_scale, (float)PyFloat_AsDouble);
    G(noise_scale, current_noise_scale, (float)PyFloat_AsDouble);
    G(noise_w, current_noise_w, (float)PyFloat_AsDouble);
    G(sentence_delay, current_sentence_delay, (float)PyFloat_AsDouble);
    G(normalize_volume, current_normalize_volume, PyObject_IsTrue);
#undef G

    PyObject *map = PyObject_GetAttrString(cfg, "phoneme_id_map");
    if (!map) return NULL;
    current_phoneme_id_map.clear();
    PyObject *key, *value; Py_ssize_t pos = 0;
    while (PyDict_Next(map, &pos, &key, &value)) {
        unsigned long cp = PyLong_AsUnsignedLong(key);
        if (PyErr_Occurred()) break;
        std::vector<PhonemeId> ids;
        for (Py_ssize_t i = 0; i < PyList_GET_SIZE(value); i++) {
            unsigned long id = PyLong_AsUnsignedLong(PyList_GET_ITEM(value, i));
            if (PyErr_Occurred()) break;
            ids.push_back(id);
        }
        current_phoneme_id_map[cp] = ids;
    }
    Py_CLEAR(map);
    if (PyErr_Occurred()) return NULL;

    // Load onnx model
    Py_BEGIN_ALLOW_THREADS;
    Ort::SessionOptions opts;
    opts.DisableCpuMemArena();
    opts.DisableMemPattern();
    opts.DisableProfiling();
    Ort::Env ort_env{ORT_LOGGING_LEVEL_WARNING, "piper"};
    ort_env.DisableTelemetryEvents();
    for (const auto& p : available_providers) {
        std::unordered_map<std::string, std::string> provider_options;
        opts.AppendExecutionProvider(p, provider_options);
    }
    session.reset();
    long long st;
    if (PRINT_TIMING_INFORMATION) st = now();
#ifdef _WIN32
    wchar_t *model_path = PyUnicode_AsWideCharString(pymp, NULL);
    if (!model_path) return NULL;
    session = std::make_unique<Ort::Session>(Ort::Session(ort_env, model_path, opts));
    PyMem_Free(model_path);
#else
    session = std::make_unique<Ort::Session>(Ort::Session(ort_env, PyUnicode_AsUTF8(pymp), opts));
#endif
    if (PRINT_TIMING_INFORMATION) { printf("model loading time: %f\n", (now()-st) / 1e9); fflush(stdout); }
    Py_END_ALLOW_THREADS;


    Py_RETURN_NONE;
}

static PyObject*
normalize(const char *text) {
    PyObject *t = PyUnicode_FromString(text);
    if (!t) return NULL;
    if (PyTuple_SetItem(normalize_data.args, 1, t) != 0) {
        Py_DECREF(t);
        return NULL;
    }
    return PyObject_CallObject(normalize_data.func, normalize_data.args);
}

static PyObject*
start(PyObject *self, PyObject *args) {
    const char *text;
    if (!PyArg_ParseTuple(args, "s", &text)) return NULL;
    if (!voice_set || session.get() == NULL) { PyErr_SetString(PyExc_Exception, "must call set_voice() first"); return NULL; }
    // Clear state
    while (!phoneme_id_queue.empty()) phoneme_id_queue.pop();
    chunk_samples.clear();

    // Convert to phonemes
    std::vector<std::string> sentence_phonemes{""};
    Py_BEGIN_ALLOW_THREADS;
    std::size_t current_idx = 0;
    const void *text_ptr = text;
    while (text_ptr != nullptr) {
        int terminator = 0;
        const char *phonemes = espeak_TextToPhonemesWithTerminator(
                &text_ptr, espeakCHARS_UTF8, espeakPHONEMES_IPA, &terminator);
        if (phonemes) sentence_phonemes[current_idx] += phonemes;
        const char *terminator_str = categorize_terminator(terminator);
        sentence_phonemes[current_idx] += terminator_str;
        if ((terminator & CLAUSE_TYPE_SENTENCE) == CLAUSE_TYPE_SENTENCE) {
            sentence_phonemes.push_back("");
            current_idx = sentence_phonemes.size() - 1;
        }
    }
    Py_END_ALLOW_THREADS;

    // phonemes to ids
    std::vector<PhonemeId> sentence_ids;
    for (auto &phonemes_str : sentence_phonemes) {
        if (phonemes_str.empty()) continue;
        sentence_ids.push_back(ID_BOS);
        sentence_ids.push_back(ID_PAD);

        PyObject *normalized_text = normalize(phonemes_str.c_str());
        if (!normalized_text) return NULL;
        int kind = PyUnicode_KIND(normalized_text); void *data = PyUnicode_DATA(normalized_text);

        // Filter out (lang) switch (flags).
        // These surround words from languages other than the current voice.
        bool in_lang_flag = false;
        for (Py_ssize_t i = 0; i < PyUnicode_GET_LENGTH(normalized_text); i++) {
            char32_t ch = PyUnicode_READ(kind, data, i);
            if (in_lang_flag) {
                if (ch == U')') {
                    // End of (lang) switch
                    in_lang_flag = false;
                }
            } else if (ch == U'(') {
                // Start of (lang) switch
                in_lang_flag = true;
            } else {
                // Look up ids
                auto ids_for_phoneme = current_phoneme_id_map.find(ch);
                if (ids_for_phoneme != current_phoneme_id_map.end()) {
                    for (auto id : ids_for_phoneme->second) {
                        sentence_ids.push_back(id);
                        sentence_ids.push_back(ID_PAD);
                    }
                }
            }
        }
        Py_CLEAR(normalized_text);
        sentence_ids.push_back(ID_EOS);
        phoneme_id_queue.emplace(std::move(sentence_ids));
        sentence_ids.clear();
    }
    Py_RETURN_NONE;
}

static PyObject*
next(PyObject *self, PyObject *args) {
    int as_16bit_samples = 1;
    if (!PyArg_ParseTuple(args, "|p", &as_16bit_samples)) return NULL;
    if (phoneme_id_queue.empty()) return Py_BuildValue("yiiO", "", 0, current_sample_rate, Py_True);
    std::vector<Ort::Value> output_tensors;
    std::vector<Ort::Value> input_tensors;

    Py_BEGIN_ALLOW_THREADS;
    // Process next list of phoneme ids
    auto next_ids = std::move(phoneme_id_queue.front());
    phoneme_id_queue.pop();

    auto memoryInfo = Ort::MemoryInfo::CreateCpu(
        OrtAllocatorType::OrtArenaAllocator, OrtMemType::OrtMemTypeDefault);

    // Allocate
    std::vector<int64_t> phoneme_id_lengths{(int64_t)next_ids.size()};
    std::vector<float> scales{current_noise_scale, current_length_scale, current_noise_w};

    std::vector<int64_t> phoneme_ids_shape{1, (int64_t)next_ids.size()};
    input_tensors.push_back(Ort::Value::CreateTensor<int64_t>(
        memoryInfo, next_ids.data(), next_ids.size(), phoneme_ids_shape.data(),
        phoneme_ids_shape.size()));

    std::vector<int64_t> phoneme_id_lengths_shape{
        (int64_t)phoneme_id_lengths.size()};
    input_tensors.push_back(Ort::Value::CreateTensor<int64_t>(
        memoryInfo, phoneme_id_lengths.data(), phoneme_id_lengths.size(),
        phoneme_id_lengths_shape.data(), phoneme_id_lengths_shape.size()));

    std::vector<int64_t> scales_shape{(int64_t)scales.size()};
    input_tensors.push_back(Ort::Value::CreateTensor<float>(
        memoryInfo, scales.data(), scales.size(), scales_shape.data(),
        scales_shape.size()));

    // Add speaker id.
    // NOTE: These must be kept outside the "if" below to avoid being
    // deallocated.
    std::vector<int64_t> speaker_id{(int64_t)0};
    std::vector<int64_t> speaker_id_shape{(int64_t)speaker_id.size()};

    if (current_num_speakers > 1) {
        input_tensors.push_back(Ort::Value::CreateTensor<int64_t>(
            memoryInfo, speaker_id.data(), speaker_id.size(),
            speaker_id_shape.data(), speaker_id_shape.size()));
    }

    // From export_onnx.py
    std::array<const char *, 4> input_names = {"input", "input_lengths", "scales", "sid"};
    std::array<const char *, 1> output_names = {"output"};

    // Infer
    Ort::RunOptions ro;
    long long st;
    if (PRINT_TIMING_INFORMATION) st = now();
    output_tensors = session->Run(
        ro, input_names.data(), input_tensors.data(),
        input_tensors.size(), output_names.data(), output_names.size());
    if (PRINT_TIMING_INFORMATION) { printf("model run time: %f\n", (now()-st) / 1e9); fflush(stdout); }
    Py_END_ALLOW_THREADS;

    if ((output_tensors.size() != 1) || (!output_tensors.front().IsTensor())) {
        PyErr_SetString(PyExc_ValueError, "failed to infer audio data from list of phoneme ids");
        return NULL;
    }

    int num_samples; const float *audio_tensor_data;
    PyObject *ans = NULL, *data = NULL;
    int num_of_silence_samples = 0;
    auto audio_shape = output_tensors.front().GetTensorTypeAndShapeInfo().GetShape();
    num_samples = (int)audio_shape[audio_shape.size() - 1];
    audio_tensor_data = output_tensors.front().GetTensorData<float>();
    float maxval = 1.f;

    Py_BEGIN_ALLOW_THREADS;
    if (current_sentence_delay > 0) num_of_silence_samples = (int)(current_sample_rate * current_sentence_delay);
    if (num_samples) {
        maxval = std::abs(audio_tensor_data[0]); float q;
        for (int i = 1; i < num_samples; i++) if ((q = std::abs(audio_tensor_data[i])) > maxval) maxval = q;
        if (maxval <= 1e-8) maxval = 1.f;
    }
    Py_END_ALLOW_THREADS;
    if (as_16bit_samples) {
        data = PyBytes_FromStringAndSize(NULL, sizeof(int16_t) * (num_samples + num_of_silence_samples));
        if (data) {
            Py_BEGIN_ALLOW_THREADS;
            int16_t *x = (int16_t*)PyBytes_AS_STRING(data);
            for (int i = 0; i < num_samples; i++) {
                x[i] = (int16_t)((audio_tensor_data[i]/maxval) * std::numeric_limits<int16_t>::max());
            }
            memset(x + num_samples, 0, num_of_silence_samples * sizeof(int16_t));
            Py_END_ALLOW_THREADS;
       }
    } else {
        data = PyBytes_FromStringAndSize(NULL, sizeof(float) * (num_samples * num_of_silence_samples));
        if (data) {
            Py_BEGIN_ALLOW_THREADS;
            float *x = (float*)PyBytes_AS_STRING(data);
            for (int i = 0; i < num_samples; i++) x[i] = audio_tensor_data[i]/maxval;
            memset(x + num_samples, 0, num_of_silence_samples * sizeof(int16_t));
            Py_END_ALLOW_THREADS;
        }
    }
    if (data) {
        ans = Py_BuildValue(
            "OiiO", data, num_samples, current_sample_rate, phoneme_id_queue.empty() ? Py_True : Py_False);
        Py_DECREF(data);
    }

    // Clean up
    for (std::size_t i = 0; i < output_tensors.size(); i++) {
        Ort::detail::OrtRelease(output_tensors[i].release());
    }
    for (std::size_t i = 0; i < input_tensors.size(); i++) {
        Ort::detail::OrtRelease(input_tensors[i].release());
    }
    return ans;
}

// Boilerplate {{{
static char doc[] = "Text to speech using the Piper TTS models";
static PyMethodDef methods[] = {
    {"initialize", (PyCFunction)initialize, METH_VARARGS,
     "initialize(espeak_data_dir) -> Initialize this module. Must be called once before using any other functions from this module. If espeak_data_dir is not specified or is the empty string the default data location is used."
    },
    {"set_voice", (PyCFunction)set_voice, METH_VARARGS,
     "set_voice(voice_config, model_path) -> Load the model in preparation for synthesis."
    },
    {"start", (PyCFunction)start, METH_VARARGS,
     "start(text) -> Start synthesizing the specified text, call next() repeatedly to get the audiodata."
    },
    {"next", (PyCFunction)next, METH_VARARGS,
     "next(as_16bit_samples=True) -> Return the next chunk of audio data (audio_data, num_samples, sample_rate, is_last). Here audio_data is a bytes object consisting of either native 16bit integer audio samples or native floats in the range [-1, 1]."
    },

    {"set_espeak_voice_by_name", (PyCFunction)set_espeak_voice_by_name, METH_O,
     "set_espeak_voice_by_name(name) -> Set the voice to be used to phonemize text"
    },
    {"phonemize", (PyCFunction)phonemize, METH_O,
     "phonemize(text) -> Convert the specified text into espeak-ng phonemes"
    },
    {NULL}  /* Sentinel */
};

static int
exec_module(PyObject *mod) {
    return 0;
}

static PyModuleDef_Slot slots[] = { {Py_mod_exec, (void*)exec_module}, {0, NULL} };

static struct PyModuleDef module_def = {PyModuleDef_HEAD_INIT};

static void
cleanup_module(void*) {
    if (initialized) {
        initialized = false;
        voice_set = false;
        espeak_Terminate();
    }
    current_phoneme_id_map.clear();
    session.reset();
    Py_CLEAR(normalize_data.func); Py_CLEAR(normalize_data.args);
}

CALIBRE_MODINIT_FUNC PyInit_piper(void) {
	module_def.m_name = "piper";
	module_def.m_slots = slots;
	module_def.m_doc = doc;
	module_def.m_methods = methods;
    module_def.m_free = cleanup_module;
	return PyModuleDef_Init(&module_def);
}
// }}}
