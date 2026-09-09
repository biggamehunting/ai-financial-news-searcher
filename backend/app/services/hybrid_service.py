from app.services.rag_service import vector_store
from app.services.bm25_service import bm25_search

from langchain_core.tools import tool

from app.services.rag_service import vector_store
from app.services.bm25_service import bm25_search
from app.services.reranker_service import rerank_documents
from app.services.confidence_service import calculate_confidence

@tool
def search_internal_knowledge(question: str) -> str:
    """
    Search only the internal documents provided to the application.

    Uses vector search + BM25 + Cohere reranking.

    Do NOT use this tool for current, public, or internet information.
    """
    print("🔵 INTERNAL RAG TOOL CALLED:", question)
    try:

        if not question or not question.strip():
            return "No valid question was provided."

        results, candidate_count, rerank_scores  = hybrid_search(
            question,
            k=5,
            top_n=3,
        )
        confidence, confidence_level = calculate_confidence(rerank_scores)

        print("RERANK SCORES:", rerank_scores)
        print("CONFIDENCE:", confidence)
        print("CONFIDENCE LEVEL:", confidence_level)
        if not results:
            return "No relevant internal information was found."

        for i, result in enumerate(results):
            print("\n==============================")
            print("RESULT TYPE:", type(result))
            print("RESULT:", result)
            print("METADATA:", getattr(result, "metadata", "NO METADATA ATTRIBUTE"))
            print("==============================")

        # for i, result in enumerate(results):

        #     print("\n==============================")
        #     print("RERANKED RESULT:", i + 1)
        #     print("==============================")

        #     print("SOURCE:", result.metadata.get("source"))
        #     print("SECTION:", result.metadata.get("section"))

        #     print("\nCONTENT:")
        #     print(result.page_content[:500])

        # return "\n\n".join(
        #     doc.page_content
        #     for doc in results
        # )
        formatted_results = []


        for i, doc in enumerate(results, start=1):
            metadata = doc.metadata or {}

            source = metadata.get("source", "Unknown")
            page = metadata.get("page")
            table_number = metadata.get("table_number")

            citation = f"[Source {i}: {source}"

            if page is not None:
                citation += f", Page {page}"

            if table_number is not None:
                citation += f", Table {table_number}"

            citation += "]"

            formatted = f"{citation}\n{doc.page_content}"

            print("\n========== RETRIEVED DOCUMENT ==========")
            print(formatted)
            print("=========================================\n")

            formatted_results.append(formatted)

        confidence_info = (
            f"[Retrieval confidence: {confidence_level} ({confidence})]\n\n"
        )

        return confidence_info + "\n\n".join(formatted_results)

    except Exception as e:
        return f"An error occurred while searching internal knowledge: {str(e)}"


def hybrid_search(question: str, k, top_n):

    print("🔵 Starting vector search...")
    vector_results = vector_store.similarity_search(
        question,
        k=k,
    )
    # for i, doc in enumerate(vector_results, start=1):
    #     print(f"\nVector {i}")
    #     print("Source:", doc.metadata.get("source"))
    #     print("Content:", doc.page_content[:200])
    print("✅ Vector search completed.")
    
    print("🟢 Starting BM25 search...")
    bm25_results = bm25_search(question)
    # for i, doc in enumerate(bm25_results, start=1):
    #     print(f"\nBM25 {i}")
    #     print("Source:", doc.metadata.get("source"))
    #     print("Content:", doc.page_content[:200])
    print("✅ BM25 search completed.")
    
    combined = vector_results + bm25_results

    unique_results = []
    seen = set()

    for doc in combined:
        key = (
            doc.metadata.get("document_id"),
            doc.page_content,
        )

        if key not in seen:
            seen.add(key)
            unique_results.append(doc)
    candidate_count = len(unique_results)
    print(f"📦 Reranker candidates: {len(unique_results)}")
    reranked_results, rerank_scores  = rerank_documents(
        question,
        unique_results,
        top_n=top_n,
    )

    return reranked_results, candidate_count, rerank_scores

@tool
def delete_payment(payment_id: str) -> str:
    """
    Delete a payment.

    This is a sensitive operation and requires human approval.
    """
    print(f"\n⚠️ APPROVAL REQUIRED: Delete payment {payment_id}?")

    approval = input("Approve? (yes/no): ").strip().lower()

    if approval != "yes":
        return f"Deletion of payment {payment_id} was rejected by the user."

    return f"Payment {payment_id} deleted successfully."



# def hybrid_search(question: str, k: int = 5):
#     # 1. Vector search
#     vector_results = vector_store.similarity_search(
#         question,
#         k=k,
#     )

#     # 2. BM25 search
#     bm25_results = bm25_search(question)

#     # 3. Combine results
#     combined = vector_results + bm25_results

#     # 4. Remove duplicate chunks
#     unique_results = []
#     seen = set()

#     for doc in combined:
#         key = (
#             doc.metadata.get("document_id"),
#             doc.page_content,
#         )

#         if key not in seen:
#             seen.add(key)
#             unique_results.append(doc)

#     return unique_results