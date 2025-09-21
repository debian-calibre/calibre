/**
 * SPDX-FileCopyrightText: (C) 2007 Dominik Seichter <domseichter@web.de>
 * SPDX-FileCopyrightText: (C) 2020 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef PDF_FONT_CACHE_H
#define PDF_FONT_CACHE_H

#include "PdfDeclarations.h"

#include "PdfFont.h"
#include "PdfEncodingFactory.h"

#ifdef PODOFO_HAVE_FONTCONFIG
#include "PdfFontConfigWrapper.h"
#endif

#if defined(_WIN32) && defined(PODOFO_HAVE_WIN32GDI)
// To have LOGFONTW available
typedef struct HFONT__* HFONT;
#endif

namespace PoDoFo {

class PdfIndirectObjectList;
class PdfResources;

struct PdfFontSearchParams
{
    nullable<PdfFontStyle> Style;
    PdfFontAutoSelectBehavior AutoSelect = PdfFontAutoSelectBehavior::None;
    PdfFontMatchBehaviorFlags MatchBehavior = PdfFontMatchBehaviorFlags::None;

    ///< A function to select the font in case multiple fonts with same characteristics found. Default return first
    std::function<PdfFont* (const std::vector<PdfFont*>)> FontSelector;
};

/**
 * This class assists PdfDocument
 * with caching font information.
 *
 * Additional to font caching, this class is also
 * responsible for font matching.
 *
 * PdfFont is an actual font that can be used in
 * a PDF file (i.e. it does also font embedding)
 * and PdfFontMetrics provides only metrics informations.
 *
 * \see PdfDocument
 */
class PODOFO_API PdfFontManager final
{
    friend class PdfDocument;
    friend class PdfMemDocument;
    friend class PdfStreamedDocument;
    friend class PdfFont;
    friend class PdfCommon;
    friend class PdfResources;

public:
    /** Get a font from the cache. If the font does not yet
     *  exist, add it to the cache.
     *
     *  \param fontPattern a search font pattern
     *  \param params font creation params
     *
     *  \returns a PdfFont object or nullptr if the font could
     *           not be created or found.
     */
    PdfFont* SearchFont(const std::string_view& fontPattern,
        const PdfFontSearchParams& searchParams = { }, const PdfFontCreateParams& createParams = { });

    PdfFont* SearchFont(const std::string_view& fontPattern, const PdfFontCreateParams& createParams);

    PdfFont& GetStandard14Font(PdfStandard14FontType stdFont,
        const PdfFontCreateParams& params = { });

    PdfFont& GetOrCreateFont(const std::string_view& fontPath, unsigned faceIndex,
        const PdfFontCreateParams& params = { });

    PdfFont& GetOrCreateFontFromBuffer(const bufferview& buffer, unsigned faceIndex,
        const PdfFontCreateParams& params = { });

    PdfFont& GetOrCreateFont(const std::string_view& fontPath,
        const PdfFontCreateParams& params = { });

    PdfFont& GetOrCreateFontFromBuffer(const bufferview& buffer,
        const PdfFontCreateParams& params = { });

    /**
     * \param face a valid freetype font face. The face is
     *        referenced and the font data is copied
     * \param params font creation params
     *
     * \returns a PdfFont object or nullptr if the font could
     *          not be created or found.
     */
    PdfFont& GetOrCreateFont(FT_Face face, const PdfFontCreateParams& params = { });

    /** Try to search for fontmetrics from the given fontname and parameters
     *
     * \returns the found metrics. Null if not found
     */
    static PdfFontMetricsConstPtr SearchFontMetrics(const std::string_view& fontPattern,
        const PdfFontSearchParams& params = { });

#if defined(_WIN32) && defined(PODOFO_HAVE_WIN32GDI)
    PdfFont& GetOrCreateFont(HFONT font, const PdfFontCreateParams& params = { });
#endif

#ifdef PODOFO_HAVE_FONTCONFIG
    /**
     * Set wrapper for the fontconfig library.
     * Useful to avoid initializing Fontconfig multiple times.
     *
     * This setter can be called until first use of Fontconfig
     * as the library is initialized at first use.
     */
    static void SetFontConfigWrapper(const std::shared_ptr<PdfFontConfigWrapper>& fontConfig);

    static PdfFontConfigWrapper& GetFontConfigWrapper();
#endif // PODOFO_HAVE_FONTCONFIG

    /** Called by PdfDocument before saving
     */
    void EmbedFonts();

    // These methods are reserved to use to selected friend classes
private:
    PdfFontManager(PdfDocument& doc);

private:
    const PdfFont* GetLoadedFont(const PdfResources& resources, const std::string_view& name);

    /**
     * Empty the internal font cache.
     * This should be done when ever a new document
     * is created or openened.
     */
    void Clear();

    PdfFont* AddImported(std::unique_ptr<PdfFont>&& font);

    /** Returns a new ABCDEF+ like font subset prefix
     */
    std::string GenerateSubsetPrefix();

    static void AddFontDirectory(const std::string_view& path);

private:
    /** A private structure, which represents a cached font
     */
    struct Descriptor
    {
        Descriptor(const std::string_view& name, PdfStandard14FontType stdType,
            const PdfEncoding& encoding, bool hasFontStyle, PdfFontStyle style);

        Descriptor(const Descriptor& rhs) = default;
        Descriptor& operator=(const Descriptor& rhs) = default;

        std::string Name;               ///< Name of the font or pattern
        PdfStandard14FontType StdType;
        size_t EncodingId;
        bool HasFontStyle;
        PdfFontStyle Style;
    };

    struct HashElement
    {
        size_t operator()(const Descriptor& elem) const;
    };

    struct EqualElement
    {
        bool operator()(const Descriptor& lhs, const Descriptor& rhs) const;
    };

    using CachedQueries = std::unordered_map<Descriptor, std::vector<PdfFont*>, HashElement, EqualElement>;

    struct Storage
    {
        bool IsLoaded;
        std::unique_ptr<PdfFont> Font;
    };

    using FontMap = std::unordered_map<PdfReference, Storage>;

    using CachedPaths = std::unordered_map<std::string, PdfFont*>;

private:
#ifdef PODOFO_HAVE_FONTCONFIG
    static std::shared_ptr<PdfFontConfigWrapper> ensureInitializedFontConfig();
#endif // PODOFO_HAVE_FONTCONFIG

    static FT_Face getFontFace(const std::string_view& fontName,
        const PdfFontSearchParams& params, std::unique_ptr<charbuff>& data,
        std::string& fontpath, unsigned& faceIndex);
    PdfFont* getImportedFont(const std::string_view& patternName,
        const PdfFontSearchParams& searchParams, const PdfFontCreateParams& createParams);
    static void adaptSearchParams(std::string& patternName,
        PdfFontSearchParams& searchParams);
    PdfFont* addImported(std::vector<PdfFont*>& fonts, std::unique_ptr<PdfFont>&& font);
    PdfFont& getOrCreateFontHashed(const std::shared_ptr<PdfFontMetrics>& metrics, const PdfFontCreateParams& params);

#if defined(_WIN32) && defined(PODOFO_HAVE_WIN32GDI)
    static std::unique_ptr<charbuff> getWin32FontData(const std::string_view& fontName,
        const PdfFontSearchParams& params);
#endif

private:
    PdfFontManager(const PdfFontManager&) = delete;
    PdfFontManager& operator=(const PdfFontManager&) = delete;

private:
    PdfDocument* m_doc;
    std::string m_currentPrefix;

    // Map of cached font queries
    CachedQueries m_cachedQueries;

    // Map of cached font paths
    CachedPaths m_cachedPaths;

    // Map of all indirect fonts
    FontMap m_fonts;

    // Map of all invalid inline fonts
    std::unordered_map<std::string, std::unique_ptr<PdfFont>> m_inlineFonts;

#ifdef PODOFO_HAVE_FONTCONFIG
    static std::shared_ptr<PdfFontConfigWrapper> m_fontConfig;
#endif
};

};

#endif // PDF_FONT_CACHE_H
