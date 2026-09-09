from app.services.hybrid_service import hybrid_search

question = "What was Voltalia's EBITDA in H1 2026?"

results, candidate_count = hybrid_search(
    question,
    k=5,
    top_n=3,
)

print("\n==============================")
print("FINAL RERANKED RESULTS")
print("==============================")

print("Candidate count:", candidate_count)

for i, doc in enumerate(results, start=1):
    print(f"\nRESULT {i}")
    print("SOURCE:", doc.metadata.get("source"))
    print("DOCUMENT ID:", doc.metadata.get("document_id"))
    print("SECTION:", doc.metadata.get("section"))
    print("CONTENT:")
    print(doc.page_content[:500])