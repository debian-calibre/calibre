# PoDoFo [![build-linux](https://github.com/podofo/podofo/actions/workflows/build-linux.yml/badge.svg)](https://github.com/podofo/podofo/actions/workflows/build-linux.yml) [![build-mac](https://github.com/podofo/podofo/actions/workflows/build-mac.yml/badge.svg)](https://github.com/podofo/podofo/actions/workflows/build-mac.yml) [![build-win](https://github.com/podofo/podofo/actions/workflows/build-win.yml/badge.svg)](https://github.com/podofo/podofo/actions/workflows/build-win.yml)

1.  [What is PoDoFo?](#what-is-podofo)
2.  [Requirements](#requirements)
3.  [Licensing](#licensing)
4.  [Development quickstart](#development-quickstart)
5.  [String encoding and buffer conventions](#string-encoding-and-buffer-conventions)
6.  [API Stability](#api-stability)
7.  [PoDoFo tools](#podofo-tools)
8.  [TODO](#todo)
9.  [FAQ](#faq)
10.  [No warranty](#no-warranty)
11.  [Contributions](#contributions)
12.  [Authors](#authors)

## What is PoDoFo?

PoDoFo is a s a free portable C++ library to work with the PDF file format.

PoDoFo provides classes to parse a PDF file and modify its content
into memory. The changes can be written back to disk easily.
Besides PDF parsing PoDoFo also provides facilities to create your
own PDF files from scratch. It currently does not
support rendering PDF content.

## Requirements

To build PoDoFo lib you'll need a c++17 compiler,
CMake 3.16 and the following libraries:

* freetype2
* fontconfig (required for Unix platforms, optional for Windows)
* OpenSSL (1.1 and 3.0 are supported)
* LibXml2
* zlib
* libjpeg (optional)
* libtiff (optional)
* libpng (optional)
* libidn (optional)

For the most polular toolchains, PoDoFo requires the following
minimum versions:

* msvc++ 14.16 (VS 2017 15.9)
* gcc 8.1
* clang/llvm 7.0

It is regularly tested with the following IDE/toolchains versions:

* Visual Studio 2017 15.9
* Visual Studio 2019 16.11
* Visual Studio 2022 17.3
* gcc 9.3.1
* XCode 13.3
* NDK r23b

## Licensing

PoDoFo library is licensed under the [LGPL 2.0](https://spdx.org/licenses/LGPL-2.0-or-later.html) or later terms.
PoDoFo tools are licensed under the [GPL 2.0](https://spdx.org/licenses/GPL-2.0-or-later.html) or later terms.

## Development quickstart

PoDoFo is known to compile through a multitude of package managers (including `apt-get`, [brew](https://brew.sh/), [vcpkg](https://vcpkg.io/), [Conan](https://conan.io/)), and has public continous integration working in [Ubuntu Linux](https://github.com/podofo/podofo/blob/master/.github/workflows/build-linux.yml), [MacOS](https://github.com/podofo/podofo/blob/master/.github/workflows/build-linux.yml) and
[Windows](https://github.com/podofo/podofo/blob/master/.github/workflows/build-win.yml), bootstrapping the CMake project, building and testing the library. It's highly recommended to build PoDoFo using such package managers. 

There's also a playground area in the repository where you can have
access to pre-build dependencies for some popular architectures/operating systems:
the playground is the recommended setting to develop the library and reproduce bugs,
while it's not recommended for the deployment of your application using PoDoFo.
Have a look to the [Readme](https://github.com/podofo/podofo/tree/master/playground) there.

> **Warning**: PoDoFo is known to be working in cross-compilation toolchains (eg. Android/iOS development), but support may not provided in such scenarios. If you decide to manually build dependencies you are assumed to know how to identity possible library clashes/mismatches and how to deal with compilation/linking problems that can arise in your system.

### Build with apt-get

From the source root run:

```
sudo apt-get install -y libfontconfig1-dev libfreetype-dev libxml2-dev libssl-dev libjpeg-dev libpng-dev libtiff-dev libidn11-dev
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . --config Debug
```

### Build with brew

Install [brew](https://brew.sh/), then from the source root run:

```
brew install fontconfig freetype openssl libxml2 jpeg-turbo libpng libtiff libidn
mkdir build
cd build
cmake  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_FIND_FRAMEWORK=NEVER -DCMAKE_PREFIX_PATH=`brew --prefix` -DFontconfig_INCLUDE_DIR=`brew --prefix fontconfig`/include -DOPENSSL_ROOT_DIR=`brew --prefix openssl@3` ..
cmake --build . --config Debug
```

### Build with Conan

Install [conan](https://docs.conan.io/1/installation.html), then from source root run:

```
mkdir build
cd build
conan install ..
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . --config Debug
```

### Build with vcpkg

Follow the vcpkg [quickstart](https://vcpkg.io/en/getting-started.html) guide to setup the package manager repository first.
In Windows, it may be also useful to set the enviroment variable `VCPKG_DEFAULT_TRIPLET` to `x64-windows` to default installing 64 bit dependencies
and define a `VCPKG_INSTALLATION_ROOT` variable with the location of the repository as created in the quickstart.

Then from source root run:

```
vcpkg install fontconfig freetype libxml2 openssl libjpeg-turbo libpng tiff zlib
mkdir build
cd build
cmake -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . --config Debug
```

### CMake switches

- `PODOFO_BUILD_TEST`: Build the unit tests, defaults to TRUE;

- `PODOFO_BUILD_EXAMPLES`: Build the examples, defaults to TRUE;

- `PODOFO_BUILD_TOOLS`: Build the PoDoFo tools, defaults to FALSE. See
the relevant [section](https://github.com/podofo/podofo/#podofo-tools) in the Readme;

- `PODOFO_BUILD_LIB_ONLY`: If TRUE, it will build only the library component.
This unconditionally disable building tests, examples and tools;

- `PODOFO_BUILD_STATIC`: If TRUE, build the library as a static object and use it in tests,
examples and tools. By default a shared library is built.

## String encoding and buffer conventions

All `std::strings` or `std::string_view` in the library are intended
to hold UTF-8 encoded string content. `PdfString` and `PdfName` constructors
accept UTF-8 encoded strings by default (`PdfName` accept only characters in the
`PdfDocEncoding` char set, though). `charbuff` abd `bufferview`
instead represent a generic octet buffer.

## API migration

PoDoFo has an unstable API that is the result of an extensive API review of PoDoFo 0.9.x. At this [link](https://github.com/podofo/podofo/wiki/PoDoFo-API-migration-guide/#098---0100) you can find an incomplete guide on migrating 0.9.8 code to 0.10.0. It is expected PoDoFo will converge to a stable API as soon as the review process is completed. See [API Stability](https://github.com/podofo/podofo/wiki/API-Stability) for more details.

## PoDoFo Tools

> **Warning**: Tools are currently **untested** and **unmaintained**.

PoDoFo tools are still available in the source [tree](https://github.com/podofo/podofo/)
but their compilation is disabled by default because they are unsted/unmaintained,
and will not receive support until their status is cleared. It's not recommended to include them in software distributions.
If you want to build them make sure to bootstrap the CMake project with ```-DPODOFO_BUILD_TOOLS=TRUE```.
Tools are conveniently enabled in the [playground](https://github.com/podofo/podofo/tree/master/playground)
at least to ensure library changes won't break their compilation.

## TODO

There's a [TODO](https://github.com/podofo/podofo/blob/master/TODO.md) list, or look
at the [issue](https://github.com/podofo/podofo/issues) tracker.

## FAQ

**Q: How do I sign a document?**

**A:** The signing procedure is still as low level as it was before the
ongoing source changes. This is going to change, soon!, with a new high-level
API for signing being worked on, which will be fully unit tested. For now you
should check the `podofosign` tool (**WARNING**: untested) which should give
you the idea how to sign documents creating a *CMS* structure directly with
OpenSSL.
To describe the procedure briefly, one has to fully Implement a `PdfSigner`,
retrieve or create a `PdfSignature` field, create an output device (see next question)
and use `PoDoFo::SignDocument(doc, device, signer, signature)`. When signing,
the sequence of calls of `PdfSignature` works in this way: method `PdfSigner::Reset()`
is called first, then  the `PdfSigner::ComputeSignature(buffer, dryrun)` is called with
an empty buffer and the `dryrun` argument set to `true`. In this call one can just
resize the buffer overestimating the required size for the signature, or just
compute a fake signature that must be saved on the buffer. Then a sequence of
`PdfSigner::AppendData(buffer)` are called, receiving all the document data to
be signed. A final `PdfSigner::ComputeSignature(buffer, dryrun)` is called, with
the `dryrun` parameter set to `false`. The buffer on this call is cleared (capacity
is not altered) or not accordingly to the value of `PdfSigner::SkipBufferClear()`.


**Q: `PdfMemDocument::SaveUpdate()` or `PoDoFo::SignDocument()` write only a partial
file: why so and why there's no mechanism to seamlessly handle the incremental
update as it was in PoDoFo? What should be done to correctly update/sign the
document?**

**A:** The previous mechanism in PoDoFo required enablement of document for
incremental updates, which is a decision step which I believe should be not
be necessary. Also:
1. In case of file loaded document it still required to perform the update in
the same file, and the check was performed on the path of the files being
operated to, which is unsafe;
2. In case of buffers worked for one update/signing operation but didn't work
for following operations.

The idea is to implement a more explicit mechanism that makes more clear
and/or enforces the fact that the incremental update must be performed on the
same file in case of file loaded documents or that underlying buffer will grow
following subsequent operations in case of buffer loaded documents.
Before that, as a workaround, a couple of examples showing the correct operation
to either update or sign a document (file or buffer loaded) are presented.
Save an update on a file loaded document, by copying the source to another
destination:

```
    string inputPath;
    string outputPath;
    auto input = std::make_shared<FileStreamDevice>(inputPath);
    FileStreamDevice output(outputPath, FileMode::Create);
    input->CopyTo(output);

    PdfMemDocument doc;
    doc.LoadFromDevice(input);

    doc.SaveUpdate(output);
```

Sign a buffer loaded document:

```
    bufferview inputBuffer;
    charbuff outputBuffer;
    auto input = std::make_shared<SpanStreamDevice>(inputBuffer);
    BufferStreamDevice output(outputBuffer);
    input->CopyTo(output);

    PdfMemDocument doc;
    doc.LoadFromDevice(input);
    // Retrieve/create the signature, create the signer, ...
    PoDoFo::SignDocument(doc, output, signer, signature);
```

**Q: Can I sign a document a second time?**

**A:** Yes, this is tested, but to make sure this will work you'll to re-parse the document a second time,
as re-using the already loaded document is still untested (this may change later). For example do as it follows:

```
    bufferview inputBuffer;
    charbuff outputBuffer;
    auto input = std::make_shared<SpanStreamDevice>(inputBuffer);
    BufferStreamDevice output(outputBuffer);
    input->CopyTo(output);

    {
        PdfMemDocument doc;
        doc.LoadFromDevice(input);
        // Retrieve/create the signature, create the signer, ...
        PoDoFo::SignDocument(doc, output, signer, signature);
    }

    input = std::make_shared<SpanStreamDevice>(output);
    {
        PdfMemDocument doc;
        doc.LoadFromDevice(input);
        // Retrieve/create the signature, create the signer, ...
        PoDoFo::SignDocument(doc, output, signer, signature);
    }
```

## No warranty

PoDoFo may or may not work for your needs and comes with absolutely no
warranty. Serious bugs, including security flaws, may be fixed at arbitrary
timeframes, or not fixed at all. Priority of implementing new features
and bug fixing are decided according to the interests and personal
preferences of the maintainers. If you need PoDoFo to integrate a feature
or bug fix that is critical to your workflow, the most welcome and fastest
approach is to [contribute](https://github.com/podofo/podofo/edit/master/README.md#contributions)
high-quality patches.

## Contributions

Please subscribe to the project mailing [list](https://sourceforge.net/projects/podofo/lists/podofo-users)
which is still followed by several of the original developers of PoDoFo.
A gitter [community](https://gitter.im/podofo/community) has also been created to ease some more informal chatter.
If you find a bug and know how to fix it, or you want to add a small feature, you're welcome to send a [pull request](https://github.com/podofo/podofo/pulls),
providing it follows the [coding style](https://github.com/podofo/podofo/blob/master/CODING-STYLE.md)
of the project. As a minimum requisite, any contribution should be:
* valuable for a multitude of people and not only self relevant for the contributor;
* consistent with surrounding code and not result in unpredictable behavior and/or bugs.

Other reasons for the rejection, or hold, of a pull request may be:

* the proposed code is incomplete or hacky;
* the change doesn't fit the scope of PoDoFo;
* the change shows lack of knowledge/mastery of the PDF specification and/or C++ language;
* the change breaks automatic tests performed by the maintainer;
* general lack of time in reviewing and merging the change.

If you need to implement a bigger feature or refactor, ask first if
it was already planned. The feature may be up for grabs, meaning that it's open for external contributions.
Please write in the relevant issue that you started to work on that, to receive some feedback/coordination.
If it's not, it means that the refactor/feature is planned to be implemented later by the maintainer(s).
If the feature is not listed in the issues, add it and/or create a [discussion](https://github.com/podofo/podofo/discussions)
to receive some feedback and discuss some basic design choices.

## Authors

> **Warning**: Please don't use personal email addresses for technical support inquries, but create
github [issues](https://github.com/podofo/podofo/issues) instead.

PoDoFo is currently developed and maintained by
[Francesco Pretto](mailto:ceztko@gmail.com), together with Dominik Seichter and others. See the file
[AUTHORS.md](https://github.com/podofo/podofo/blob/master/AUTHORS.md) for more details.

