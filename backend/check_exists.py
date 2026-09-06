from app.services.bm25_service import documents

sources = {}

for doc in documents:
    source = doc.metadata.get("source", "UNKNOWN")
    sources[source] = sources.get(source, 0) + 1

print("\nSOURCES IN CORPUS")
print("=" * 60)

for source, count in sorted(sources.items()):
    print(f"{count:3} chunks | {source}")