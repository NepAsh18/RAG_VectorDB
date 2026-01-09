from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from .embeddings import embed
from app.core.config import settings

class VectorRetriever:
    def __init__(self):
      
        self.client = QdrantClient(url=settings.QDRANT_URL)

    def search(self, query: str, filename: str = None, limit: int = 5):
        """
        Search for relevant text chunks. 
        If filename is provided, it restricts the search to that specific document.
        """
        
        vector = embed([query])[0]
        
        
        search_filter = None
        if filename:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="filename", 
                        match=MatchValue(value=filename)
                    )
                ]
            )

       
        results = self.client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=vector,
            query_filter=search_filter,
            limit=limit,
            with_payload=True
        )

        
        return [
            {
                "text": hit.payload.get("text"),
                "filename": hit.payload.get("filename"),
                "score": hit.score 
            } 
            for hit in results
        ]