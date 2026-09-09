from pdf_processor import extract_pdf_elements

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


PDF_PATH = r"C:\Users\omkar\Downloads\AI\chatbot-app 3\chatbot-app 3\backend\app\rag\documents\offer_letter_with_ctc_mock.pdf"


# ==========================================================
# 1. Extract PDF elements
# ==========================================================

elements = extract_pdf_elements(PDF_PATH)


# ==========================================================
# 2. Separate text and tables
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


# ==========================================================
# 3. Create text documents
# ==========================================================

text_documents = []

for element in text_elements:

    text_documents.append(
        Document(
            page_content=element["content"],
            metadata={
                "page": element["page"],
                "content_type": "text",
            }
        )
    )


# ==========================================================
# 4. Chunk normal text
# ==========================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

text_chunks = splitter.split_documents(
    text_documents
)


# ==========================================================
# 5. Create table chunks
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
                "page": element["page"],
                "content_type": "table",
                "table_number": element["table_number"],
            }
        )
    )


# ==========================================================
# 6. Combine
# ==========================================================

final_chunks = (
    text_chunks +
    table_chunks
)


print("Total chunks:", len(final_chunks))


# ==========================================================
# 7. Create embedding model
# ==========================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# ==========================================================
# 8. Test embedding
# ==========================================================

print("Creating embeddings...")

vectors = embeddings.embed_documents(
    [
        chunk.page_content
        for chunk in final_chunks
    ]
)


# ==========================================================
# 9. Verify
# ==========================================================

print("\n" + "=" * 60)
print("EMBEDDING TEST")
print("=" * 60)

print("Chunks:", len(final_chunks))

print("Vectors:", len(vectors))

if vectors:
    print("Vector dimension:", len(vectors[0]))

    print("\nFirst vector:")
    print(vectors[0][:10])

print("=" * 60)
print("EMBEDDING SUCCESS")
print("=" * 60)