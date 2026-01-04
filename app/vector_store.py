from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from uuid import uuid4
from app.utils import QDRANT_URL, QDRANT_COLLECTION

client = QdrantClient(url=QDRANT_URL)

def init_qdrant():
    if QDRANT_COLLECTION not in [
        c.name for c in client.get_collections().collections
    ]:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def store_vectors(chunks, embeddings, meta):
    doc_id = str(uuid4())

    points = [
        {
            "id": f"{doc_id}_{i}",
            "vector": embeddings[i],
            "payload": {
                "doc_id": doc_id,
                "text": chunks[i],
                "filename": meta["filename"]
            }
        }
        for i in range(len(chunks))
    ]

    client.upsert(QDRANT_COLLECTION, points)
    return doc_id
