from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "rag" / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name="shopstream_knowledge"
)

question = input("Ask about ShopStream: ")

results = collection.query(
    query_texts=[question],
    n_results=3,
)

documents = results["documents"][0]

print("\nAnswer:\n")
print(" ".join(documents))