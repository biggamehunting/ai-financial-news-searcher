from pdf_processor import extract_pdf_elements

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = r"C:\Users\omkar\Downloads\AI\chatbot-app 3\chatbot-app 3\backend\app\rag\documents\mock_form_16_fy_2025_26.pdf"


# ==========================================================
# 1. Extract structured PDF elements
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


print("Text elements:", len(text_elements))
print("Table elements:", len(table_elements))


# ==========================================================
# 3. Create LangChain Documents for normal text
# ==========================================================

text_documents = []

for element in text_elements:

    document = Document(
        page_content=element["content"],
        metadata={
            "page": element["page"],
            "content_type": "text",
        }
    )

    text_documents.append(document)


# ==========================================================
# 4. Chunk normal text
# ==========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)


text_chunks = text_splitter.split_documents(
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

    document = Document(
        page_content=table_text,
        metadata={
            "page": element["page"],
            "content_type": "table",
            "table_number": element["table_number"],
        }
    )

    table_chunks.append(document)


# ==========================================================
# 6. Combine chunks
# ==========================================================

final_chunks = text_chunks + table_chunks


print("\n" + "=" * 80)
print("SEARCHING FOR CTC IN CHUNKS")
print("=" * 80)

for i, chunk in enumerate(final_chunks):

    if "ctc" in chunk.page_content.lower():

        print(f"\n--- CHUNK {i} ---")
        print("Metadata:", chunk.metadata)
        print(chunk.page_content)

# ==========================================================
# 7. Print results
# ==========================================================

# print("\n" + "=" * 80)
# print("TEXT CHUNKS")
# print("=" * 80)

# for i, chunk in enumerate(text_chunks):

#     print(f"\n--- TEXT CHUNK {i} ---")
#     print("Page:", chunk.metadata["page"])
#     print(chunk.page_content)


# print("\n" + "=" * 80)
# print("TABLE CHUNKS")
# print("=" * 80)

# for i, chunk in enumerate(table_chunks):

#     print(f"\n--- TABLE CHUNK {i} ---")
#     print("Page:", chunk.metadata["page"])
#     print("Table:", chunk.metadata["table_number"])
#     print(chunk.page_content)


# print("\n" + "=" * 80)
# print("SUMMARY")
# print("=" * 80)

# print("Text chunks:", len(text_chunks))
# print("Table chunks:", len(table_chunks))
# print("Total chunks:", len(final_chunks))