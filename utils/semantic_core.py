import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_documents(documents):
    embeddings = model.encode(documents, convert_to_numpy=True)
    return embeddings

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_search(query, documents, embeddings, top_k):
    query_vector = model.encode(query, convert_to_numpy=True)
    scores = []

    for doc, emb in zip(documents, embeddings):
        score = cosine_similarity(query_vector, emb)
        scores.append((score, doc))

    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]
def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks
