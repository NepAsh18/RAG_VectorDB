from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from app.schemas.chat import ChatRequest
from app.services.rag import RAGService
from app.db.postgres import engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    models.Base.metadata.create_all(bind=engine)
    yield
    

app = FastAPI(
    title="Conversational RAG API",
    description="Local RAG using Ollama, Qdrant, and Postgres",
    lifespan=lifespan
)


def get_rag_service():
    return RAGService()

@app.post("/chat")
async def chat(
    req: ChatRequest, 
    rag: RAGService = Depends(get_rag_service)
):
    """
    Endpoint to handle both booking logic and general RAG queries.
    """
    try:
        
        response_text = rag.answer(req.session_id, req.message)
        return {"response": response_text}
        
    except Exception as e:
       
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing your request."
        )

@app.get("/health")
def health_check():
    return {"status": "healthy"}