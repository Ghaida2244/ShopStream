from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENT_PATH = BASE_DIR / "rag" / "documents" / "shopstream_knowledge.txt"
DB_PATH = BASE_DIR / "rag" / "chroma_db"


document_text = DOCUMENT_PATH.read_text(encoding="utf-8")

chunks = [
    line.strip()
    for line in document_text.splitlines()
    if line.strip()
]

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="shopstream_knowledge"
)

collection.upsert(
    ids=[f"chunk_{index}" for index in range(len(chunks))],
    documents=chunks,
)

print(f"Stored {len(chunks)} knowledge chunks in ChromaDB.")