from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import QDRANT_URL, QDRANT_API_KEY


# ==========================================================
# 1. Configuration
# ==========================================================

COLLECTION_NAME = "payment_policy_local"


# ==========================================================
# 2. Create embedding model
# ==========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# ==========================================================
# 3. Connect to Qdrant
# ==========================================================

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


# ==========================================================
# 4. Test queries
# ==========================================================

queries = [
    "How many days of paternity leave are provided?",
    "What is the annual CTC?",
]


# ==========================================================
# 5. Search Qdrant
# ==========================================================

for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    results = vector_store.similarity_search_with_score(
        query,
        k=10,
    )

    for i, (document, score) in enumerate(results):

        print(f"\n--- RESULT {i + 1} ---")

        print("Score:", score)

        print("Metadata:")
        print(document.metadata)

        print("\nContent:")
        print(document.page_content)