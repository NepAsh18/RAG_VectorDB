import requests
from app.services.retriever import VectorRetriever
from app.services.memory import ChatMemory
from app.services.booking import BookingService
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.retriever = VectorRetriever()
        self.memory = ChatMemory()
        self.booking_service = BookingService()
        # Ensure OLLAMA_URL is in your config.py (usually http://localhost:11434)
        self.ollama_url = settings.OLLAMA_URL 
        self.model = "llama3" # or "mistral", "nomic-embed-text", etc.

    def _call_ollama(self, prompt: str) -> str:
        """Helper to send prompt to local Ollama instance."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
        return response.json().get("response", "")

    def answer(self, session_id: str, query: str) -> str:
        history = self.memory.get(session_id)

        # --- STEP 1: Intent & Extraction (The "Brain" part) ---
        # We use Ollama here to decide what the user wants.
        intent_prompt = f"""
        Analyze the user query and history. 
        If the user is trying to book or providing info (like a name) for an interview, return 'BOOKING'.
        Otherwise, return 'SEARCH'.
        History: {history[-2:]}
        Query: {query}
        Intent:"""
        
        intent = self._call_ollama(intent_prompt).strip().upper()

        if "BOOKING" in intent:
            # Here, your booking_service will use Ollama again 
            # to extract the specific {name, email, date}
            return self.booking_service.process_booking(query, session_id)

        # --- STEP 2: RAG Answer (The "Narrator" part) ---
        context_chunks = self.retriever.search(query)
        context_text = "\n".join(context_chunks)

        final_prompt = f"""
        Context: {context_text}
        History: {history[-3:]}
        Question: {query}
        Answer based strictly on context:"""
        
        answer = self._call_ollama(final_prompt)

        history.append({"user": query, "assistant": answer})
        self.memory.save(session_id, history)
        return answer