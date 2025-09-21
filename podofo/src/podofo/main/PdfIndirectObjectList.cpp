/**
 * SPDX-FileCopyrightText: (C) 2005 Dominik Seichter <domseichter@web.de>
 * SPDX-FileCopyrightText: (C) 2020 Francesco Pretto <ceztko@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#include <podofo/private/PdfDeclarationsPrivate.h>
#include "PdfIndirectObjectList.h"

#include <algorithm>

#include "PdfArray.h"
#include "PdfDictionary.h"
#include "PdfMemoryObjectStream.h"
#include "PdfObject.h"
#include "PdfReference.h"
#include "PdfObjectStream.h"
#include "PdfDocument.h"

using namespace std;
using namespace PoDoFo;

static constexpr size_t MaxReserveSize = 8388607; // cf. Table C.1 in section C.2 of PDF32000_2008.pdf
static constexpr unsigned MaxXRefGenerationNum = 65535;

struct ObjectComparatorPredicate
{
public:
    inline bool operator()(const PdfObject* obj1, const PdfObject* obj2) const
    {
        return obj1->GetIndirectReference() < obj2->GetIndirectReference();
    }
};

struct ReferenceComparatorPredicate
{
public:
    inline bool operator()(const PdfReference& obj1, const PdfReference& obj2) const
    {
        return obj1 < obj2;
    }
};

//RG: 1) Should this class not be moved to the header file
class ObjectsComparator
{
public:
    ObjectsComparator(const PdfReference& ref)
        : m_ref(ref) { }

    bool operator()(const PdfObject* p1) const
    {
        return p1 ? (p1->GetIndirectReference() == m_ref) : false;
    }

private:
    ObjectsComparator() = delete;
    ObjectsComparator(const ObjectsComparator& rhs) = delete;
    ObjectsComparator& operator=(const ObjectsComparator& rhs) = delete;

private:
    const PdfReference m_ref;
};

PdfIndirectObjectList::PdfIndirectObjectList() :
    m_Document(nullptr),
    m_CanReuseObjectNumbers(true),
    m_ObjectCount(0),
    m_StreamFactory(nullptr)
{
}

PdfIndirectObjectList::PdfIndirectObjectList(PdfDocument& document) :
    m_Document(&document),
    m_CanReuseObjectNumbers(true),
    m_ObjectCount(1),
    m_StreamFactory(nullptr)
{
}

PdfIndirectObjectList::PdfIndirectObjectList(PdfDocument& document, const PdfIndirectObjectList& rhs)  :
    m_Document(&document),
    m_CanReuseObjectNumbers(rhs.m_CanReuseObjectNumbers),
    m_ObjectCount(rhs.m_ObjectCount),
    m_FreeObjects(rhs.m_FreeObjects),
    m_unavailableObjects(rhs.m_unavailableObjects),
    m_StreamFactory(nullptr)
{
    // Copy all objects from source, resetting parent and indirect reference
    for (auto obj : rhs.m_Objects)
    {
        auto newObj = new PdfObject(*obj);
        newObj->SetIndirectReference(obj->GetIndirectReference());
        newObj->SetDocument(&document);
        m_Objects.insert(newObj);
    }
}

PdfIndirectObjectList::~PdfIndirectObjectList()
{
    Clear();
}

void PdfIndirectObjectList::Clear()
{
    for (auto obj : m_Objects)
        delete obj;

    m_Objects.clear();
    m_ObjectCount = 1;
    m_StreamFactory = nullptr;
}

PdfObject& PdfIndirectObjectList::MustGetObject(const PdfReference& ref) const
{
    auto obj = GetObject(ref);
    if (obj == nullptr)
        PODOFO_RAISE_ERROR(PdfErrorCode::NoObject);

    return *obj;
}

PdfObject* PdfIndirectObjectList::GetObject(const PdfReference& ref) const
{
    auto it = m_Objects.lower_bound(ref);
    if (it == m_Objects.end() || (*it)->GetIndirectReference() != ref)
        return nullptr;

    return *it;
}

unique_ptr<PdfObject> PdfIndirectObjectList::RemoveObject(const PdfReference& ref)
{
    return RemoveObject(ref, true);
}

unique_ptr<PdfObject> PdfIndirectObjectList::RemoveObject(const PdfReference& ref, bool markAsFree)
{
    auto it = m_Objects.lower_bound(ref);
    if (it == m_Objects.end() || (*it)->GetIndirectReference() != ref)
        return nullptr;

    return removeObject(it, markAsFree);
}

unique_ptr<PdfObject> PdfIndirectObjectList::RemoveObject(const iterator& it)
{
    return removeObject(it, true);
}

unique_ptr<PdfObject> PdfIndirectObjectList::ReplaceObject(const PdfReference& ref, PdfObject* obj)
{
    if (obj == nullptr)
        PODOFO_RAISE_ERROR_INFO(PdfErrorCode::InvalidHandle, "Object must be non null");

    auto it = m_Objects.lower_bound(ref);
    if (it == m_Objects.end())
        PODOFO_RAISE_ERROR_INFO(PdfErrorCode::InvalidHandle, "Unable to find object with reference {}", ref.ToString());

    auto hintpos = it;
    hintpos++;
    auto node = m_Objects.extract(it);
    unique_ptr<PdfObject> ret(node.value());
    node.value() = obj;
    obj->SetIndirectReference(ref);
    pushObject(hintpos, node, obj);
    return ret;
}

unique_ptr<PdfObject> PdfIndirectObjectList::removeObject(const iterator& it, bool markAsFree)
{
    auto obj = *it;
    if (m_objectStreams.find(obj->GetIndirectReference().ObjectNumber()) != m_objectStreams.end())
        PODOFO_RAISE_ERROR_INFO(PdfErrorCode::InternalLogic, "Can't remove a compressed object stream");

    if (markAsFree)
        SafeAddFreeObject(obj->GetIndirectReference());

    m_Objects.erase(it);
    return unique_ptr<PdfObject>(obj);
}

PdfReference PdfIndirectObjectList::getNextFreeObject()
{
    // Try to first use list of free objects
    if (m_CanReuseObjectNumbers && !m_FreeObjects.empty())
    {
        PdfReference freeObjectRef = m_FreeObjects.front();
        m_FreeObjects.pop_front();
        return freeObjectRef;
    }

    // If no free objects are available, create a new object with generation 0
    uint32_t nextObjectNum = static_cast<uint32_t>(m_ObjectCount);
    while (true)
    {
        if ((size_t)(nextObjectNum + 1) == MaxReserveSize)
            PODOFO_RAISE_ERROR_INFO(PdfErrorCode::ValueOutOfRange, "Reached the maximum number of indirect objects");

        // Check also if the object number it not available,
        // e.g. it reached maximum generation number (65535)
        if (m_unavailableObjects.find(nextObjectNum) == m_unavailableObjects.end())
            break;

        nextObjectNum++;
    }

    return PdfReference(nextObjectNum, 0);
}

PdfObject& PdfIndirectObjectList::CreateDictionaryObject(const string_view& type,
    const string_view& subtype)
{
    auto dict = PdfDictionary();
    if (!type.empty())
        dict.AddKey(PdfName::KeyType, PdfName(type));

    if (!subtype.empty())
        dict.AddKey(PdfName::KeySubtype, PdfName(subtype));

    auto ret = new PdfObject(std::move(dict));
    ret->setDirty();
    addNewObject(ret);
    return *ret;
}

PdfObject& PdfIndirectObjectList::CreateArrayObject()
{
    auto ret = new PdfObject(PdfArray());
    ret->setDirty();
    addNewObject(ret);
    return *ret;
}

PdfObject& PdfIndirectObjectList::CreateObject(const PdfObject& obj)
{
    auto ret = new PdfObject(obj);
    ret->setDirty();
    addNewObject(ret);
    return *ret;
}

PdfObject& PdfIndirectObjectList::CreateObject(PdfObject&& obj)
{
    auto ret = new PdfObject(std::move(obj));
    ret->setDirty();
    addNewObject(ret);
    return *ret;
}

int32_t PdfIndirectObjectList::SafeAddFreeObject(const PdfReference& reference)
{
    // From 3.4.3 Cross-Reference Table:
    // "When an indirect object is deleted, its cross-reference
    // entry is marked free and it is added to the linked list
    // of free entries.The entry’s generation number is incremented by
    // 1 to indicate the generation number to be used the next time an
    // object with that object number is created. Thus, each time
    // the entry is reused, it is given a new generation number."
    return tryAddFreeObject(reference.ObjectNumber(), reference.GenerationNumber() + 1);
}

bool PdfIndirectObjectList::TryAddFreeObject(const PdfReference& reference)
{
    return tryAddFreeObject(reference.ObjectNumber(), reference.GenerationNumber()) != -1;
}

int32_t PdfIndirectObjectList::tryAddFreeObject(uint32_t objnum, uint32_t gennum)
{
    // Documentation 3.4.3 Cross-Reference Table states: "The maximum
    // generation number is 65535; when a cross reference entry reaches
    // this value, it is never reused."
    // NOTE: gennum is uint32 to accomodate overflows from callers
    if (gennum >= MaxXRefGenerationNum)
    {
        m_unavailableObjects.insert(gennum);
        return -1;
    }

    AddFreeObject(PdfReference(objnum, (uint16_t)gennum));
    return gennum;
}

void PdfIndirectObjectList::AddFreeObject(const PdfReference& reference)
{
    auto it = std::equal_range(m_FreeObjects.begin(), m_FreeObjects.end(), reference, ReferenceComparatorPredicate());
    if (it.first != it.second && !m_FreeObjects.empty())
    {
        // Be sure that no reference is added twice to free list
        PoDoFo::LogMessage(PdfLogSeverity::Debug, "Adding {} to free list, is already contained in it!", reference.ObjectNumber());
        return;
    }
    else
    {
        // Insert so that list stays sorted
        m_FreeObjects.insert(it.first, reference);

        // When append free objects from external doc we need plus one number objects
        TryIncrementObjectCount(reference);
    }
}

void PdfIndirectObjectList::AddObjectStream(uint32_t objectNum)
{
    m_objectStreams.insert(objectNum);
}

void PdfIndirectObjectList::addNewObject(PdfObject* obj)
{
    PdfReference ref = getNextFreeObject();
    obj->SetIndirectReference(ref);
    PushObject(obj);
}

void PdfIndirectObjectList::PushObject(PdfObject* obj)
{
    obj->SetDocument(m_Document);

    ObjectList::node_type node;
    auto it = m_Objects.find(obj);
    auto hintpos = it;
    if (it != m_Objects.end())
    {
        // Delete existing object and replace
        // the pointer on its node
        hintpos++;
        node = m_Objects.extract(it);
        delete node.value();
        node.value() = obj;
    }

    pushObject(hintpos, node, obj);
}

void PdfIndirectObjectList::pushObject(const ObjectList::const_iterator& hintpos, ObjectList::node_type& node, PdfObject* obj)
{
    if (node.empty())
        m_Objects.insert(hintpos, obj);
    else
        m_Objects.insert(hintpos, std::move(node));
    TryIncrementObjectCount(obj->GetIndirectReference());
}

void PdfIndirectObjectList::CollectGarbage()
{
    if (m_Document == nullptr)
        return;

    unordered_set<PdfReference> referencedOjects;
    visitObject(m_Document->GetTrailer().GetObject(), referencedOjects);
    vector<PdfObject*> objectsToDelete;
    ObjectList newlist;
    for (PdfObject* obj : m_Objects)
    {
        auto& ref = obj->GetIndirectReference();
        if (referencedOjects.find(ref) == referencedOjects.end()
            && m_objectStreams.find(ref.ObjectNumber()) == m_objectStreams.end())
        {
            SafeAddFreeObject(ref);
            objectsToDelete.push_back(obj);
            continue;
        }

        newlist.insert(obj);
    }

    for (auto obj : objectsToDelete)
        delete obj;

    m_Objects.swap(newlist);
}

void PdfIndirectObjectList::visitObject(const PdfObject& obj, unordered_set<PdfReference>& referencedObjects)
{
    switch (obj.GetDataType())
    {
        case PdfDataType::Reference:
        {
            // Try to check if the object has been already visited
            auto indirectReference = obj.GetReferenceUnsafe();
            auto inserted = referencedObjects.insert(indirectReference);
            if (!inserted.second)
            {
                // The object has been visited, just return
                break;
            }

            auto childObj = GetObject(indirectReference);
            if (childObj == nullptr)
                break;

            visitObject(*childObj, referencedObjects);
            break;
        }
        case PdfDataType::Array:
        {
            auto& arr = obj.GetArrayUnsafe();
            for (auto& child : arr)
                visitObject(child, referencedObjects);
            break;
        }
        case PdfDataType::Dictionary:
        {
            auto& dict = obj.GetDictionaryUnsafe();
            for (auto& pair : dict)
                visitObject(pair.second, referencedObjects);
            break;
        }
        default:
        {
            // Nothing to do
            break;
        }
    }
}

void PdfIndirectObjectList::Detach(Observer& observer)
{
    auto it = m_observers.begin();
    while (it != m_observers.end())
    {
        if (*it == &observer)
        {
            m_observers.erase(it);
            break;
        }
        else
        {
            it++;
        }
    }
}

unique_ptr<PdfObjectStreamProvider> PdfIndirectObjectList::CreateStream()
{
    if (m_StreamFactory == nullptr)
    {
        return unique_ptr<PdfObjectStreamProvider>(
            new PdfMemoryObjectStream());
    }
    else
    {
        return m_StreamFactory->CreateStream();
    }
}

void PdfIndirectObjectList::WriteObject(PdfObject& obj)
{
    // Tell any observers that there are new objects to write
    for (auto& observer : m_observers)
        observer->WriteObject(obj);
}

void PdfIndirectObjectList::Finish()
{
    // always work on a copy of the vector
    // in case a child invalidates our iterators
    // with a call to attach or detach.
    ObserverList copy(m_observers);
    for (auto& observer : copy)
        observer->Finish();
}

void PdfIndirectObjectList::BeginAppendStream(PdfObjectStream& stream)
{
    for (auto& observer : m_observers)
        observer->BeginAppendStream(stream);
}

void PdfIndirectObjectList::EndAppendStream(PdfObjectStream& stream)
{
    for (auto& observer : m_observers)
        observer->EndAppendStream(stream);
}

void PdfIndirectObjectList::SetCanReuseObjectNumbers(bool canReuseObjectNumbers)
{
    m_CanReuseObjectNumbers = canReuseObjectNumbers;

    if (!m_CanReuseObjectNumbers)
        m_FreeObjects.clear();
}

unsigned PdfIndirectObjectList::GetSize() const
{
    return (unsigned)m_Objects.size();
}

void PdfIndirectObjectList::Attach(Observer& observer)
{
    m_observers.push_back(&observer);
}

void PdfIndirectObjectList::SetStreamFactory(StreamFactory* factory)
{
    m_StreamFactory = factory;
}

void PdfIndirectObjectList::TryIncrementObjectCount(const PdfReference& ref)
{
    if (ref.ObjectNumber() >= m_ObjectCount)
    {
        // "m_ObjectCount" is used for the next free object number.
        // We need to use the greatest object number + 1 for the next free object number.
        // Otherwise, object number overlap would have occurred.
        m_ObjectCount = ref.ObjectNumber() + 1;
    }
}

PdfIndirectObjectList::iterator PdfIndirectObjectList::begin() const
{
    return m_Objects.begin();
}

PdfIndirectObjectList::iterator PdfIndirectObjectList::end() const
{
    return m_Objects.end();
}

PdfIndirectObjectList::reverse_iterator PdfIndirectObjectList::rbegin() const
{
    return m_Objects.rbegin();
}

PdfIndirectObjectList::reverse_iterator PdfIndirectObjectList::rend() const
{
    return m_Objects.rend();
}

size_t PdfIndirectObjectList::size() const
{
    return m_Objects.size();
}
