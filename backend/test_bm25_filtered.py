from app.services.bm25_service import bm25_search

question = "What was Voltalia EBITDA in H1 2026?"

results = bm25_search(
    question,
    document_id="earnings-call-transcript-voltalia-posts-stronger-h1-2026-ebitda-stock-falls-by-investing"
)

print("\nFILTERED RESULTS")

for i, doc in enumerate(results):
    print("\nRESULT:", i + 1)
    print("SOURCE:", doc.metadata.get("source"))
    print("DOCUMENT:", doc.metadata.get("document_id"))
    print(doc.page_content[:300])