import os
import re
import uuid

from pdf_processor import extract_pdf_elements

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import PointIdsList

from app.config import QDRANT_URL, QDRANT_API_KEY


# ==========================================================
# 1. File to ingest
# ==========================================================

file_path = (
    r"C:\Users\omkar\Downloads\AI\chatbot-app 3"
    r"\chatbot-app 3\backend\app\rag\documents"
    r"\mock_form_16_fy_2025_26.pdf"
)

COLLECTION_NAME = "payment_policy_local"


# ==========================================================
# 2. Create document identity
# ==========================================================

file_name = os.path.basename(file_path)

source = os.path.splitext(file_name)[0]

source = re.sub(
    r"\s+",
    " ",
    source
).strip()

document_key = re.sub(
    r"[^a-zA-Z0-9]+",
    "-",
    source
).strip("-").lower()


print("=" * 60)
print("DOCUMENT")
print("=" * 60)

print("File:", file_name)
print("Source:", source)
print("Document key:", document_key)


# ==========================================================
# 3. Extract PDF elements
# ==========================================================

print("\nExtracting PDF...")

elements = extract_pdf_elements(file_path)

print(
    "PDF extraction completed."
)

print(
    "Total elements:",
    len(elements)
)


# ==========================================================
# 4. Separate text and tables
# ==========================================================

text_elements = [
    element
    for element in elements
    if element["type"] == "text"
]

table_elements = [
    element
    for element in elements
    if element["type"] == "table"
]

print(
    "Text elements:",
    len(text_elements)
)

print(
    "Table elements:",
    len(table_elements)
)


# ==========================================================
# 5. Create normal text documents
# ==========================================================

text_documents = []

for element in text_elements:

    text_documents.append(
        Document(
            page_content=element["content"],
            metadata={
                "source": source,
                "document_id": document_key,
                "page": element["page"],
                "content_type": "text",
            }
        )
    )


# ==========================================================
# 6. Chunk normal text
# ==========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

text_chunks = text_splitter.split_documents(
    text_documents
)

print(
    "\nText chunks:",
    len(text_chunks)
)


# ==========================================================
# 7. Create table chunks
# ==========================================================

table_chunks = []

for element in table_elements:

    table_text = (
        f"TABLE {element['table_number']}\n"
        f"{element['content']}"
    )

    table_chunks.append(
        Document(
            page_content=table_text,
            metadata={
                "source": source,
                "document_id": document_key,
                "page": element["page"],
                "content_type": "table",
                "table_number": element["table_number"],
            }
        )
    )


print(
    "Table chunks:",
    len(table_chunks)
)


# ==========================================================
# 8. Combine chunks
# ==========================================================

final_chunks = (
    text_chunks +
    table_chunks
)

print(
    "Total chunks:",
    len(final_chunks)
)


# ==========================================================
# 9. Add chunk index
# ==========================================================

for i, chunk in enumerate(final_chunks):

    chunk.metadata["chunk_index"] = i


# ==========================================================
# 10. Create embedding model
# ==========================================================

print("\nCreating embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# ==========================================================
# 11. Connect to existing Qdrant collection
# ==========================================================

print("Connecting to Qdrant...")

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

print("Connected to Qdrant.")


# ==========================================================
# 12. Find existing points for THIS document
# ==========================================================

print(
    "\nChecking existing points for this document..."
)

offset = None
existing_ids = []

while True:

    points, offset = vector_store.client.scroll(
        collection_name=COLLECTION_NAME,
        limit=100,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )

    for point in points:

        payload = point.payload or {}

        metadata = payload.get(
            "metadata",
            {}
        )

        if metadata.get("source") == source:

            existing_ids.append(
                point.id
            )

    if offset is None:
        break


print(
    "Existing points:",
    len(existing_ids)
)


# ==========================================================
# 13. Delete previous version of THIS document
# ==========================================================

if existing_ids:

    print(
        "\nDeleting previous version..."
    )

    vector_store.client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=PointIdsList(
            points=existing_ids
        ),
    )

    print(
        "Deleted",
        len(existing_ids),
        "old points."
    )

else:

    print(
        "No previous version found."
    )


# ==========================================================
# 14. Create deterministic UUIDs
# ==========================================================

ids = []

for i in range(len(final_chunks)):

    chunk_id = uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"{document_key}-chunk-{i}"
    )

    ids.append(
        str(chunk_id)
    )


# ==========================================================
# 15. Upload chunks in batches
# ==========================================================

batch_size = 10

print("\nStarting upload...")

for i in range(
    0,
    len(final_chunks),
    batch_size
):

    batch = final_chunks[
        i:i + batch_size
    ]

    batch_ids = ids[
        i:i + len(batch)
    ]

    print(
        f"Uploading chunks "
        f"{i + 1} to "
        f"{i + len(batch)} "
        f"of {len(final_chunks)}..."
    )

    vector_store.add_documents(
        batch,
        ids=batch_ids,
    )


# ==========================================================
# 16. Verify Qdrant
# ==========================================================

print(
    "\nChecking final collection size..."
)

collection_info = vector_store.client.get_collection(
    COLLECTION_NAME
)


print("=" * 60)
print("INGESTION COMPLETED")
print("=" * 60)

print("Document:", source)
print("Text chunks:", len(text_chunks))
print("Table chunks:", len(table_chunks))
print("Total new chunks:", len(final_chunks))
print(
    "Points after ingestion:",
    collection_info.points_count
)

print("=" * 60)