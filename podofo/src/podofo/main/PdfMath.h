/**
 * SPDX-FileCopyrightText: (C) 2021 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 * SPDX-License-Identifier: MPL-2.0
 */

#ifndef PDF_MATH_H
#define PDF_MATH_H

#include "PdfDeclarations.h"
#include <podofo/auxiliary/Rect.h>
#include <podofo/auxiliary/Matrix.h>

namespace PoDoFo
{
    class PdfPage;

    /**
     * Get a rotation trasformation that aligns the rectangle to the axis after the rotation
     */
    Matrix PODOFO_API GetFrameRotationTransform(const Rect& rect, double teta);

    /**
     * Get an inverse rotation trasformation that aligns the rectangle to the axis after the rotation
     */
    Matrix PODOFO_API GetFrameRotationTransformInverse(const Rect& rect, double teta);

    /**
     * Transform the given rect accordingly to the page rotation
     * \param inputIsTransformed if true the input rectangle is already transformed,
     *   if false the input is canonically oriented in top-right quandrant
     */
    Rect PODOFO_API TransformRectPage(const Rect& rect, const PdfPage& page, bool inputIsTransformed);
}

#endif // PDF_MATH_H
