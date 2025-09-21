/**
 * SPDX-FileCopyrightText: (C) 2006 Dominik Seichter <domseichter@web.de>
 * SPDX-FileCopyrightText: (C) 2020 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef AUX_RECT_H
#define AUX_RECT_H

#include "basedefs.h"

namespace PoDoFo {

class PdfArray;
class Matrix;

/** A rectangle defined by position and size
 */
class PODOFO_API Rect final
{
public:
    double X;
    double Y;
    double Width;
    double Height;

public:
    /** Create an empty rectangle with bottom=left=with=height=0
     */
    Rect();

    /** Create a rectangle with a given size and position
     */
    Rect(double x, double y, double width, double height);

    /** Copy constructor
     */
    Rect(const Rect& rhs) = default;

public:
    /** Create a Rect from a couple of arbitrary points
     * \returns the created Rect
     */
    static Rect FromCorners(double x1, double y1, double x2, double y2);

    /** Create a Rect from a the 4 values in the array
     *  \param arr the array to load the values from
     */
    static Rect FromArray(const PdfArray& arr);

    /** Converts the rectangle into an array
     *  \param var the array to store the Rect
     */
    void ToArray(PdfArray& arr) const;

    /** Returns a string representation of the Rect
     * \returns std::string representation as [ left bottom right top ]
     */
    std::string ToString() const;

    bool Contains(double x, double y) const;

    // REMOVE-ME: The name of this method is bad and it's also
    /** Intersect with another rect
     *  \param rect the rect to intersect with
     */
    void Intersect(const Rect& rect);

public:
    /** Get the left coordinate of the rectangle
     */
    double GetLeft() const { return X; }

    /** Get the bottom coordinate of the rectangle
     */
    double GetBottom() const { return Y; }

    /** Get the right coordinate of the rectangle
     */
    double GetRight() const;

    /** Get the top coordinate of the rectangle
     */
    double GetTop() const;

public:
    bool operator==(const Rect& rect) const;
    bool operator!=(const Rect& rect) const;

public:
    Rect operator*(const Matrix& m) const;
    Rect& operator=(const Rect& rhs) = default;
};

};

#endif // AUX_RECT_H
