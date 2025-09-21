/**
 * SPDX-FileCopyrightText: (C) 2022 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 * SPDX-License-Identifier: MPL-2.0
 */

#include <podofo/private/PdfDeclarationsPrivate.h>
#include "PdfAnnotation_Types.h"

#include "PdfDictionary.h"
#include "PdfFileSpec.h"

using namespace std;
using namespace PoDoFo;

void PdfAnnotationLink::SetDestination(const shared_ptr<PdfDestination>& destination)
{
    destination->AddToDictionary(GetDictionary());
    m_Destination = destination;
}

shared_ptr<PdfDestination> PdfAnnotationLink::GetDestination() const
{
    return const_cast<PdfAnnotationLink&>(*this).getDestination();
}

shared_ptr<PdfDestination> PdfAnnotationLink::getDestination()
{
    if (m_Destination == nullptr)
    {
        auto obj = GetDictionary().FindKey("Dest");
        if (obj == nullptr)
            return nullptr;

        m_Destination.reset(new PdfDestination(*obj));
    }

    return m_Destination;
}

void PdfAnnotationFileAttachement::SetFileAttachement(const shared_ptr<PdfFileSpec>& fileSpec)
{
    GetDictionary().AddKey("FS", fileSpec->GetObject().GetIndirectReference());
    m_FileSpec = fileSpec;
}

shared_ptr<PdfFileSpec> PdfAnnotationFileAttachement::GetFileAttachement() const
{
    return const_cast<PdfAnnotationFileAttachement&>(*this).getFileAttachment();
}

shared_ptr<PdfFileSpec> PdfAnnotationFileAttachement::getFileAttachment()
{
    if (m_FileSpec == nullptr)
    {
        auto obj = GetDictionary().FindKey("FS");
        if (obj == nullptr)
            return nullptr;

        m_FileSpec.reset(new PdfFileSpec(*obj));
    }

    return m_FileSpec;
}

void PdfAnnotationPopup::SetOpen(const nullable<bool>& value)
{
    if (value.has_value())
        GetDictionary().AddKey("Open", *value);
    else
        GetDictionary().RemoveKey("Open");
}

bool PdfAnnotationPopup::GetOpen() const
{
    return GetDictionary().GetKeyAs<bool>("Open", false);
}

void PdfAnnotationText::SetOpen(const nullable<bool>& value)
{
    if (value.has_value())
        GetDictionary().AddKey("Open", *value);
    else
        GetDictionary().RemoveKey("Open");
}

bool PdfAnnotationText::GetOpen() const
{
    return GetDictionary().GetKeyAs<bool>("Open", false);
}

PdfAnnotationTextMarkupBase::PdfAnnotationTextMarkupBase(PdfPage& page, PdfAnnotationType annotType, const Rect& rect)
    : PdfAnnotation(page, annotType, rect)
{
}

PdfAnnotationTextMarkupBase::PdfAnnotationTextMarkupBase(PdfObject& obj, PdfAnnotationType annotType)
    : PdfAnnotation(obj, annotType)
{
}

PdfAnnotationLink::PdfAnnotationLink(PdfPage& page, const Rect& rect)
    : PdfAnnotationActionBase(page, PdfAnnotationType::Link, rect)
{
}

PdfAnnotationLink::PdfAnnotationLink(PdfObject& obj)
    : PdfAnnotationActionBase(obj, PdfAnnotationType::Link)
{
}

PdfAnnotationPopup::PdfAnnotationPopup(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Popup, rect)
{
}

PdfAnnotationPopup::PdfAnnotationPopup(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Popup)
{
}

PdfAnnotationText::PdfAnnotationText(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Text, rect)
{
}

PdfAnnotationText::PdfAnnotationText(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Text)
{
}

PdfAnnotationCaret::PdfAnnotationCaret(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Caret, rect)
{
}

PdfAnnotationCaret::PdfAnnotationCaret(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Caret)
{
}

PdfAnnotationFileAttachement::PdfAnnotationFileAttachement(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::FileAttachement, rect)
{
}

PdfAnnotationFileAttachement::PdfAnnotationFileAttachement(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::FileAttachement)
{
}

PdfAnnotationFreeText::PdfAnnotationFreeText(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::FreeText, rect)
{
}

PdfAnnotationFreeText::PdfAnnotationFreeText(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::FreeText)
{
}

PdfAnnotationHighlight::PdfAnnotationHighlight(PdfPage& page, const Rect& rect)
    : PdfAnnotationTextMarkupBase(page, PdfAnnotationType::Highlight, rect)
{
}

PdfAnnotationHighlight::PdfAnnotationHighlight(PdfObject& obj)
    : PdfAnnotationTextMarkupBase(obj, PdfAnnotationType::Highlight)
{
}

PdfAnnotationInk::PdfAnnotationInk(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Ink, rect)
{
}

PdfAnnotationInk::PdfAnnotationInk(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Ink)
{
}

PdfAnnotationLine::PdfAnnotationLine(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Line, rect)
{
}

PdfAnnotationLine::PdfAnnotationLine(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Line)
{
}

PdfAnnotationModel3D::PdfAnnotationModel3D(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Model3D, rect)
{
}

PdfAnnotationModel3D::PdfAnnotationModel3D(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Model3D)
{
}

PdfAnnotationMovie::PdfAnnotationMovie(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Movie, rect)
{
}

PdfAnnotationMovie::PdfAnnotationMovie(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Movie)
{
}

PdfAnnotationPolygon::PdfAnnotationPolygon(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Polygon, rect)
{
}

PdfAnnotationPolygon::PdfAnnotationPolygon(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Polygon)
{
}

PdfAnnotationPolyLine::PdfAnnotationPolyLine(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::PolyLine, rect)
{
}

PdfAnnotationPolyLine::PdfAnnotationPolyLine(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::PolyLine)
{
}

PdfAnnotationPrinterMark::PdfAnnotationPrinterMark(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::PrinterMark, rect)
{
}

PdfAnnotationPrinterMark::PdfAnnotationPrinterMark(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::PrinterMark)
{
}

PdfAnnotationRichMedia::PdfAnnotationRichMedia(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::RichMedia, rect)
{
}

PdfAnnotationRichMedia::PdfAnnotationRichMedia(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::RichMedia)
{
}

PdfAnnotationScreen::PdfAnnotationScreen(PdfPage& page, const Rect& rect)
    : PdfAnnotationActionBase(page, PdfAnnotationType::Screen, rect)
{
}

PdfAnnotationScreen::PdfAnnotationScreen(PdfObject& obj)
    : PdfAnnotationActionBase(obj, PdfAnnotationType::Screen)
{
}

PdfAnnotationSquiggly::PdfAnnotationSquiggly(PdfPage& page, const Rect& rect)
    : PdfAnnotationTextMarkupBase(page, PdfAnnotationType::Squiggly, rect)
{
}

PdfAnnotationSquiggly::PdfAnnotationSquiggly(PdfObject& obj)
    : PdfAnnotationTextMarkupBase(obj, PdfAnnotationType::Squiggly)
{
}

PdfAnnotationStrikeOut::PdfAnnotationStrikeOut(PdfPage& page, const Rect& rect)
    : PdfAnnotationTextMarkupBase(page, PdfAnnotationType::StrikeOut, rect)
{
}

PdfAnnotationStrikeOut::PdfAnnotationStrikeOut(PdfObject& obj)
    : PdfAnnotationTextMarkupBase(obj, PdfAnnotationType::StrikeOut)
{
}

PdfAnnotationSound::PdfAnnotationSound(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Sound, rect)
{
}

PdfAnnotationSound::PdfAnnotationSound(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Sound)
{
}

PdfAnnotationSquare::PdfAnnotationSquare(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Square, rect)
{
}

PdfAnnotationSquare::PdfAnnotationSquare(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Square)
{
}

PdfAnnotationCircle::PdfAnnotationCircle(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Circle, rect)
{
}

PdfAnnotationCircle::PdfAnnotationCircle(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Circle)
{
}

PdfAnnotationStamp::PdfAnnotationStamp(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Stamp, rect)
{
}

PdfAnnotationStamp::PdfAnnotationStamp(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Stamp)
{
}

PdfAnnotationTrapNet::PdfAnnotationTrapNet(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::TrapNet, rect)
{
}

PdfAnnotationTrapNet::PdfAnnotationTrapNet(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::TrapNet)
{
}

PdfAnnotationUnderline::PdfAnnotationUnderline(PdfPage& page, const Rect& rect)
    : PdfAnnotationTextMarkupBase(page, PdfAnnotationType::Underline, rect)
{
}

PdfAnnotationUnderline::PdfAnnotationUnderline(PdfObject& obj)
    : PdfAnnotationTextMarkupBase(obj, PdfAnnotationType::Underline)
{
}

PdfAnnotationWatermark::PdfAnnotationWatermark(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Watermark, rect)
{
}

PdfAnnotationWatermark::PdfAnnotationWatermark(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Watermark)
{
}

PdfAnnotationWebMedia::PdfAnnotationWebMedia(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::WebMedia, rect)
{
}

PdfAnnotationWebMedia::PdfAnnotationWebMedia(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::WebMedia)
{
}

PdfAnnotationRedact::PdfAnnotationRedact(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Redact, rect)
{
}

PdfAnnotationRedact::PdfAnnotationRedact(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Redact)
{
}

PdfAnnotationProjection::PdfAnnotationProjection(PdfPage& page, const Rect& rect)
    : PdfAnnotation(page, PdfAnnotationType::Projection, rect)
{
}

PdfAnnotationProjection::PdfAnnotationProjection(PdfObject& obj)
    : PdfAnnotation(obj, PdfAnnotationType::Projection)
{
}
