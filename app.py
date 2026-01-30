from sentence_transformers import SentenceTransformer
import numpy as np

# Try importing Endee safely
try:
    from endee import Endee
    endee_available = True
    db = Endee()
    print("✅ Endee initialized")
except Exception as e:
    endee_available = False
    print("⚠️ Endee initialized with limited support")

# ---------------- SETUP ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents
with open("data/documents.txt", "r") as file:
    documents = [line.strip() for line in file if line.strip()]

print(f"📄 Loaded {len(documents)} documents")

# Encode documents
embeddings = model.encode(documents, convert_to_numpy=True)

stored_vectors = []

for doc, vector in zip(documents, embeddings):
    stored_vectors.append((vector, doc))

    # Use Endee only if add exists
    if endee_available and hasattr(db, "add"):
        try:
            db.add(vector=vector, metadata={"text": doc})
        except Exception:
            pass  # Safe fallback

print("✅ Vectors prepared")

# ---------------- SEMANTIC SEARCH ----------------

query = input("\n🔍 Enter your search query: ")

query_vector = model.encode(query, convert_to_numpy=True)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

results = []

for vector, text in stored_vectors:
    score = cosine_similarity(query_vector, vector)
    results.append((score, text))

# Sort by similarity
results.sort(key=lambda x: x[0], reverse=True)

print("\n📄 Search Results:")
for i, (score, text) in enumerate(results[:2], start=1):
    print(f"{i}. {text}  (score: {score:.3f})")
