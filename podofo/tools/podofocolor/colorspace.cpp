/**
 * SPDX-FileCopyrightText: (C) 2010 Dominik Seichter <domseichter@web.de>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include <podofo/private/PdfDeclarationsPrivate.h>
#include "colorspace.h"

using namespace PoDoFo;

ColorSpace::ColorSpace()
    : m_name("DeviceGray")
{
}
    
ColorSpace::ColorSpace(const PdfName & rName)
    : m_name(rName)
{
}
    
ColorSpace::ColorSpace(const ColorSpace & rhs)
{
    this->operator=(rhs);
}

ColorSpace::~ColorSpace()
{
}
    
const ColorSpace & ColorSpace::operator=(const ColorSpace & rhs)
{
    m_name = rhs.m_name;
    return *this;
}

bool ColorSpace::IsSimpleColorSpace() const
{
    PdfColorSpace colorSpace = this->ConvertToPdfColorSpace();

    if( colorSpace == PdfColorSpace::DeviceGray
        || colorSpace == PdfColorSpace::DeviceRGB
        || colorSpace == PdfColorSpace::DeviceCMYK )
    {
        return true;
    }
    else
    {
        return false;
    }
}

PdfColorSpace ColorSpace::ConvertToPdfColorSpace() const
{
    return PoDoFo::NameToColorSpaceRaw(m_name);
}
