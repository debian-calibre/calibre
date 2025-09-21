/**
 * Copyright (C) 2009 by Dominik Seichter <domseichter@web.de>
 * Copyright (C) 2021 by Francesco Pretto <ceztko@gmail.com>
 *
 * Licensed under GNU Library General Public 2.0 or later.
 * Some rights reserved. See COPYING, AUTHORS.
 */

#include <PdfTest.h>

#include <podofo/private/FreetypePrivate.h>

using namespace std;
using namespace PoDoFo;

#ifdef PODOFO_HAVE_FONTCONFIG

#include <fontconfig/fontconfig.h>

static bool getFontInfo(FcPattern* font, string& fontFamily, string& fontPath,
    PdfFontStyle& style);
static void testSingleFont(FcPattern* font);

TEST_CASE("TestFonts")
{
    // Get all installed fonts
    auto pattern = FcPatternCreate();
    auto objectSet = FcObjectSetBuild(FC_FAMILY, FC_STYLE, FC_FILE, FC_SLANT, FC_WEIGHT, nullptr);
    auto fontSet = FcFontList(nullptr, pattern, objectSet);

    FcObjectSetDestroy(objectSet);
    FcPatternDestroy(pattern);

    if (fontSet == nullptr)
    {
        INFO("Unable to search for fonts");
        return;
    }

    INFO(utls::Format("Testing {} fonts", fontSet->nfont));
    for (int i = 0; i < fontSet->nfont; i++)
        testSingleFont(fontSet->fonts[i]);

    FcFontSetDestroy(fontSet);
}

TEST_CASE("TestCreateFontExtract")
{
    PdfMemDocument doc;
    auto& page = doc.GetPages().CreatePage(PdfPage::CreateStandardPageSize(PdfPageSize::A4));

    // Play a bit with font path caching
    auto fontPath1 = TestUtils::GetTestInputFilePath("Fonts", "LiberationSans-Regular.ttf");
    auto fontPath2 = TestUtils::GetTestInputFilePath("Fonts", "..", "Fonts", "LiberationSans-Regular.ttf");
    auto fontRef = &doc.GetFonts().GetOrCreateFont(fontPath1);
    auto& font = doc.GetFonts().GetOrCreateFont(fontPath2);
    PdfFont* fontFromBuffer;

    {
        charbuff fontbuffer;
        utls::ReadTo(fontbuffer, TestUtils::GetTestInputFilePath("Fonts", "LiberationSans-Regular.ttf"));
        fontFromBuffer = &doc.GetFonts().GetOrCreateFontFromBuffer(fontbuffer);
    }

    // The matched fonts should be the same one
    REQUIRE(&font == fontRef);

    {
        PdfPainter painter;
        painter.SetCanvas(page);

        painter.TextState.SetFont(font, 30.0);
        painter.DrawText("ěščř", 100, 600);

        painter.TextState.SetFont(*fontFromBuffer, 30.0);
        painter.DrawText("ěščř buffer", 100, 500);
        painter.FinishDrawing();
    }

    auto outputpath = TestUtils::GetTestOutputFilePath("TestCreateFontExtract.pdf");

    try
    {
        FileStreamDevice stream(outputpath, FileMode::Create);
        doc.Save(stream);
    }
    catch (const PdfError& error)
    {
        // Don't continue further the test in this case
        if (error.GetCode() == PdfErrorCode::UnsupportedFontFormat)
            return;

        throw;
    }

    // FIXME: The test crash if we tried to extract
    // text directly on the original "doc" page

    PdfMemDocument doc2;
    doc2.Load(outputpath);

    vector<PdfTextEntry> entries;
    doc2.GetPages().GetPageAt(0).ExtractTextTo(entries);

    REQUIRE(entries[0].Text == "ěščř");
    REQUIRE(entries[0].X == 100);
    REQUIRE(entries[0].Y == 600);

    REQUIRE(entries[1].Text == "ěščř buffer");
    REQUIRE(entries[1].X == 100);
    REQUIRE(entries[1].Y == 500);
}

void testSingleFont(FcPattern* font)
{
    PdfMemDocument doc;
    string fontFamily;
    string fontPath;
    PdfFontStyle style;
    PdfFontConfigSearchParams fcParams;
    auto& fcWrapper = PdfFontManager::GetFontConfigWrapper();

    if (getFontInfo(font, fontFamily, fontPath, style))
    {
        unsigned faceIndex;
        fcParams.Style = style;
        fontPath = fcWrapper.SearchFontPath(fontFamily, fcParams, faceIndex);
        if (fontPath.length() != 0)
        {
            PdfFontSearchParams params;
            params.Style = style;
            (void)doc.GetFonts().SearchFont(fontFamily, params);
            INFO(utls::Format("Font failed: {}", fontPath));
        }
    }
}

bool getFontInfo(FcPattern* font, string& fontFamily, string& fontPath,
    PdfFontStyle& style)
{
    FcChar8* family = nullptr;
    FcChar8* path = nullptr;
    int slant;
    int weight;
    style = PdfFontStyle::Regular;

    if (FcPatternGetString(font, FC_FAMILY, 0, &family) == FcResultMatch)
    {
        fontFamily = reinterpret_cast<char*>(family);
        if (FcPatternGetString(font, FC_FILE, 0, &path) == FcResultMatch)
        {
            fontPath = reinterpret_cast<char*>(path);

            if (FcPatternGetInteger(font, FC_SLANT, 0, &slant) == FcResultMatch)
            {
                if (slant == FC_SLANT_ITALIC || slant == FC_SLANT_OBLIQUE)
                    style |= PdfFontStyle::Italic;

                if (FcPatternGetInteger(font, FC_WEIGHT, 0, &weight) == FcResultMatch)
                {
                    if (weight >= FC_WEIGHT_BOLD)
                        style |= PdfFontStyle::Bold;

                    return true;
                }
            }
            //free( file );
        }
        //free( family );
    }

    return false;
}

#endif // PODOFO_HAVE_FONTCONFIG
