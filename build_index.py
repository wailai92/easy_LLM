import os
import requests
import chromadb

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "embeddinggemma"
DOCS_DIR = "documents"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"


def get_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "input": text
        },
        timeout=120
    )
    response.raise_for_status()
    data = response.json()
    return data["embeddings"][0]


def chunk_text(text: str, chunk_size: int = 300) -> list[str]:
    lines = text.splitlines()
    chunks = []
    current = []

    for line in lines:
        if not line.strip():
            continue

        current.append(line.strip())
        joined = " ".join(current)

        if len(joined) >= chunk_size:
            chunks.append(joined)
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def main():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    doc_id = 0

    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DOCS_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)

            collection.add(
                ids=[f"doc_{doc_id}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": filename,
                    "chunk_index": idx
                }]
            )
            doc_id += 1

    print("Index build complete.")

