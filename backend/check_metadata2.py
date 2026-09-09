from app.services.rag_service import vector_store

points, _ = vector_store.client.scroll(
    collection_name="payment_policy_local",
    limit=5,
    with_payload=True,
    with_vectors=False,
)

for point in points:
    print("\n====================")
    print("ID:", point.id)
    print("PAYLOAD:")
    print(point.payload)