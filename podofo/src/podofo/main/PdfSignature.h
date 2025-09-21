/**
 * SPDX-FileCopyrightText: (C) 2011 Dominik Seichter <domseichter@web.de>
 * SPDX-FileCopyrightText: (C) 2011 Petr Pytelka
 * SPDX-FileCopyrightText: (C) 2020 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef PDF_SIGNATURE_H
#define PDF_SIGNATURE_H

#include "PdfDeclarations.h"

#include "PdfAnnotation.h"
#include "PdfField.h"
#include "PdfDate.h"
#include "PdfData.h"

namespace PoDoFo {

class PdfAcroForm;

enum class PdfCertPermission
{
    NoPerms = 1,
    FormFill = 2,
    Annotations = 3,
};

struct PdfSignatureBeacons
{
    PdfSignatureBeacons();
    charbuff ContentsBeacon;
    charbuff ByteRangeBeacon;
    std::shared_ptr<size_t> ContentsOffset;
    std::shared_ptr<size_t> ByteRangeOffset;
};

class PODOFO_API PdfSignature : public PdfField
{
    friend class PdfField;

private:
    PdfSignature(PdfAcroForm& acroform, const std::shared_ptr<PdfField>& parent);

    PdfSignature(PdfAnnotationWidget& widget, const std::shared_ptr<PdfField>& parent);

    PdfSignature(PdfObject& obj, PdfAcroForm* acroform);

public:
    /** Set an appearance stream for this signature field
     *  to specify its visual appearance
     *  \param obj an XObject
     *  \param appearance an appearance type to set
     *  \param state the state for which set it the obj; states depend on the annotation type
     */
    void SetAppearanceStream(PdfXObjectForm& obj, PdfAppearanceType appearance = PdfAppearanceType::Normal, const PdfName& state = "");

    /** Create space for signature
     *
     * Structure of the PDF file - before signing:
     * <</ByteRange[ 0 1234567890 1234567890 1234567890]/Contents<signatureData>
     * Have to be replaiced with the following structure:
     * <</ByteRange[ 0 count pos count]/Contents<real signature ...0-padding>
     *
     * \param filter /Filter for this signature
     * \param subFilter /SubFilter for this signature
     * \param subFilter /Type for this signature
     * \param beacons Shared sentinels that will updated
     *                during writing of the document
     */
    void PrepareForSigning(const std::string_view& filter,
        const std::string_view& subFilter,
        const std::string_view& type,
        const PdfSignatureBeacons& beacons);

    /** Set the signer name
    *
    *  \param text the signer name
    */
    void SetSignerName(nullable<const PdfString&> text);

    /** Set reason of the signature
     *
     *  \param text the reason of signature
     */
    void SetSignatureReason(nullable<const PdfString&> text);

    /** Set location of the signature
     *
     *  \param text the location of signature
     */
    void SetSignatureLocation(nullable<const PdfString&> text);

    /** Set the creator of the signature
     *
     *  \param creator the creator of the signature
     */
    void SetSignatureCreator(nullable<const PdfString&> creator);

    /** Date of signature
     */
    void SetSignatureDate(nullable<const PdfDate&> sigDate);

    /** Add certification dictionaries and references to document catalog.
     *
     *  \param perm document modification permission
     */
    void AddCertificationReference(PdfCertPermission perm = PdfCertPermission::NoPerms);

    /** Get the signer name
    *
    *  \returns the found signer object
    */
    nullable<const PdfString&> GetSignerName() const;

    /** Get the reason of the signature
    *
    *  \returns the found reason object
    */
    nullable<const PdfString&> GetSignatureReason() const;

    /** Get the location of the signature
    *
    *  \returns the found location object
    */
    nullable<const PdfString&> GetSignatureLocation() const;

    /** Get the date of the signature
    *
    *  \returns the found date object
    */
    nullable<PdfDate> GetSignatureDate() const;

    /** Ensures that the signature field has set a signature object.
     *  The function does nothing, if the signature object is already
     *  set. This is useful for cases when the signature field had been
     *  created from an existing annotation, which didn't have it set.
     */
    void EnsureValueObject();

    PdfSignature* GetParent();
    const PdfSignature* GetParent() const;

protected:
    PdfObject* getValueObject() const;

private:
    void init(PdfAcroForm& acroForm);

private:
    PdfObject* m_ValueObj;
};

}

#endif // PDF_SIGNATURE_H
