/**
 * SPDX-FileCopyrightText: (C) 2007 Dominik Seichter <domseichter@web.de>
 * SPDX-FileCopyrightText: (C) 2020 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef PDF_FONT_CID_TRUE_TYPE_H
#define PDF_FONT_CID_TRUE_TYPE_H

#include "PdfFontCID.h"

namespace PoDoFo {

/** A PdfFont that represents a CID-keyed font that has a TrueType font backend
 */
class PdfFontCIDTrueType final : public PdfFontCID
{
    friend class PdfFont;

private:
    /** Create a new CID font.
     *
     *  \param parent parent of the font object
     *  \param metrics pointer to a font metrics object. The font in the PDF
     *         file will match this fontmetrics object. The metrics object is
     *         deleted along with the font.
     *  \param encoding the encoding of this font
     */
    PdfFontCIDTrueType(PdfDocument& doc, const PdfFontMetricsConstPtr& metrics,
        const PdfEncoding& encoding);

public:
    PdfFontType GetType() const override;

protected:
    void embedFontSubset() override;
};

};

#endif // PDF_FONT_CID_TRUE_TYPE_H
