from fastapi import FastAPI, Query
from app.loader import load_documents
from app.chunker import fixed_chunking, semantic_chunking
from app.embeddings import embed
from app.vector_store import store_vectors, init_qdrant
from app.db import SessionLocal, documents
from app.utils import DATA_DIR

app = FastAPI(title="Document Ingestion API")

init_qdrant()

@app.post("/ingest")
def ingest(chunking: str = Query("fixed", enum=["fixed", "semantic"])):
    db = SessionLocal()
    results = []

    for doc in load_documents(DATA_DIR):
        chunks = (
            fixed_chunking(doc["text"])
            if chunking == "fixed"
            else semantic_chunking(doc["text"])
        )

        vectors = embed(chunks)
        doc_id = store_vectors(chunks, vectors, doc)

        db.execute(documents.insert().values(
            id=doc_id,
            filename=doc["filename"],
            file_type=doc["file_type"],
            author=doc["author"],
            chunk_count=len(chunks)
        ))
        db.commit()

        results.append({"id": doc_id, "chunks": len(chunks)})

    db.close()
    return results


@app.get("/")
def health():
    return {"status": "ok"}
