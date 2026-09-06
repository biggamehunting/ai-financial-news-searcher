from app.services.hybrid_service import hybrid_search
import time


TEST_QUESTIONS = [
    {
        "question": "What was Voltalia's EBITDA in H1 2026?",
        "expected_answer": "EUR 110 million",
    },
    {
        "question": "How much did Voltalia's EBITDA increase year over year in H1 2026?",
        "expected_answer": "35%",
    },
    {
        "question": "What was Voltalia's turnover in H1 2026?",
        "expected_answer": "EUR 331 million",
    },
    {
        "question": "What was Voltalia's net loss attributable to the group?",
        "expected_answer": "EUR 43 million",
    },
    {
        "question": "How much Brazilian curtailment compensation did Voltalia book in H1 2026?",
        "expected_answer": "EUR 29 million",
    },
    {
        "question": "What was Voltalia's operating cash flow in H1 2026?",
        "expected_answer": "EUR 102 million",
    },
    {
        "question": "What was Voltalia's cash position?",
        "expected_answer": "EUR 343 million",
    },
    {
        "question": "What was Voltalia's cost of debt?",
        "expected_answer": "6.3%",
    },
    {
        "question": "What was Voltalia's 2026 EBITDA guidance?",
        "expected_answer": "EUR 210 million to EUR 230 million",
    },
    {
        "question": "What was Voltalia's 2027 EBITDA target?",
        "expected_answer": "EUR 300 million to EUR 325 million",
    },
]


K_VALUES = [5,10]
total_candidates = 0
total_latency = 0
for k in K_VALUES:

    hits = 0
    
    
    print("\n" + "=" * 60)
    print(f"TESTING k = {k}")
    print("=" * 60)

    K_VALUES = [5, 10]

for k in K_VALUES:

    hits = 0
    total_candidates = 0
    total_latency = 0

    print("\n" + "=" * 60)
    print(f"TESTING k = {k}")
    print("=" * 60)

    for test in TEST_QUESTIONS:

        question = test["question"]
        expected_answer = test["expected_answer"]

        retrieval_start = time.time()

        results, candidate_count = hybrid_search(
            question,
            k=k,
            top_n=3,
        )

        retrieval_latency = time.time() - retrieval_start

        print(f"📦 Reranker candidates: {candidate_count}")
        print(f"⏱️ Retrieval latency: {retrieval_latency:.2f}s")

        # Aggregate values
        total_candidates += candidate_count
        total_latency += retrieval_latency

        # Check answer
        retrieved_text = " ".join(
            doc.page_content.lower()
            for doc in results
        )

        hit = expected_answer.lower() in retrieved_text

        if hit:
            hits += 1
            print("✅ HIT:", question)
        else:
            print("❌ MISS:", question)

        time.sleep(10)

    # Calculate metrics for this k
    hit_rate = hits / len(TEST_QUESTIONS)

    average_candidates = (
        total_candidates / len(TEST_QUESTIONS)
    )

    average_latency = (
        total_latency / len(TEST_QUESTIONS)
    )

    print("\n" + "-" * 60)
    print(f"RESULTS FOR k = {k}")
    print("-" * 60)

    print(f"Hit@3: {hit_rate:.2%}")
    print(f"Average reranker candidates: {average_candidates:.2f}")
    print(f"Average latency: {average_latency:.2f} seconds")