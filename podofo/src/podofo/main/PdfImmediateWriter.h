/**
 * SPDX-FileCopyrightText: (C) 2007 Dominik Seichter <domseichter@web.de>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef PDF_IMMEDIATE_WRITER_H
#define PDF_IMMEDIATE_WRITER_H

#include "PdfDeclarations.h"
#include "PdfIndirectObjectList.h"
#include "PdfWriter.h"

namespace PoDoFo {

class PdfEncrypt;
class OutputStreamDevice;
class PdfXRef;

/** A kind of PdfWriter that writes objects with streams immediately to
 *  an OutputStreamDevice
 */
class PODOFO_API PdfImmediateWriter : private PdfWriter,
    private PdfIndirectObjectList::Observer,
    private PdfIndirectObjectList::StreamFactory
{
public:
    /** Create a new PdfWriter that writes objects with streams immediately to an OutputStreamDevice
     *
     *  This has the advantage that large documents can be created without
     *  having to keep the whole document in memory.
     *
     *  \param device all stream streams are immediately written to this output device
     *                 while the document is created.
     *  \param objects a vector of objects containing the objects which are written to disk
     *  \param trailer the trailer object
     *  \param version the PDF version of the document to write.
     *                      The PDF version can only be set in the constructor
     *                      as it is the first item written to the document on disk.
     *  \param encrypt pointer to an encryption object or nullptr. If not nullptr
     *                  the PdfEncrypt object will be copied and used to encrypt the
     *                  created document.
     *  \param writeMode additional options for writing the pdf
     */
    PdfImmediateWriter(PdfIndirectObjectList& objects, const PdfObject& trailer, OutputStreamDevice& device,
        PdfVersion version = PdfVersion::V1_5, PdfEncrypt* encrypt = nullptr,
        PdfSaveOptions opts = PdfSaveOptions::None);

    ~PdfImmediateWriter();

public:
    /** Get the write mode used for writing the PDF
     *  \returns the write mode
     */
    PdfWriteFlags GetWriteFlags() const;

    /** Get the PDF version of the document
     *  The PDF version can only be set in the constructor
     *  as it is the first item written to the document on disk
     *
     *  \returns PdfVersion version of the pdf document
     */
    PdfVersion GetPdfVersion() const;

private:
    void WriteObject(const PdfObject& obj) override;
    void Finish() override;
    void BeginAppendStream(PdfObjectStream& stream) override;
    void EndAppendStream(PdfObjectStream& stream) override;
    std::unique_ptr<PdfObjectStreamProvider> CreateStream() override;

    /** Assume the stream for the last object has
     *  been written complete.
     *  Therefore close the stream of the object
     *  now so that the next object can be written
     *  to disk
     */
    void FinishLastObject();

private:
    bool m_attached;
    OutputStreamDevice* m_Device;
    std::unique_ptr<PdfXRef> m_xRef;
    PdfObject* m_Last;
    bool m_OpenStream;
};

};

#endif // PDF_IMMEDIATE_WRITER_H
