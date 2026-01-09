import ollama
from typing import List

def embed(texts: List[str]) -> List[List[float]]:
    if isinstance(texts, str):
        texts = [texts]

    embeddings = []
    for text in texts:
        response = ollama.embeddings(
            model="nomic-embed-text",
            input=text
        )
        embeddings.append(response["embedding"])

    return embeddings
