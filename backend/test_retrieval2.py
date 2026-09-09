from app.services.hybrid_service import hybrid_search


questions = [
    # "What is the basic salary in my Form 16?",
    # "What is the standard deduction in my Form 16?",
    "What is the HRA exemption in my Form 16?",
    # "What is the TDS deducted by my employer?",
    # "What is the Gross CTC in my offer letter?",
]


for question in questions:
    print("\n" + "=" * 80)
    print("QUESTION:", question)
    print("=" * 80)

    results, candidate_count = hybrid_search(
        question,
        k=5,
        top_n=3
    )

    print("\nCandidate count:", candidate_count)

    print("\nFINAL RERANKED RESULTS:")

    for i, doc in enumerate(results, start=1):
        print(f"\n--- RESULT {i} ---")
        print("SOURCE:", doc.metadata.get("source"))
        print("PAGE:", doc.metadata.get("page"))
        print("TABLE:", doc.metadata.get("table_number"))
        print("CONTENT:")
        print(doc.page_content)