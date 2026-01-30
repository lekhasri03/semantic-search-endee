from sentence_transformers import SentenceTransformer
import numpy as np

# Try importing Endee safely
try:
    from endee import Endee
    db = Endee()
    endee_available = True
    print("✅ Endee initialized")
except Exception:
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

    if endee_available and hasattr(db, "add"):
        try:
            db.add(vector=vector, metadata={"text": doc})
        except Exception:
            pass

print("✅ Vectors prepared successfully")

# ---------------- UTILITY FUNCTIONS ----------------

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def semantic_search(query, top_k):
    query_vector = model.encode(query, convert_to_numpy=True)
    results = []

    for vector, text in stored_vectors:
        score = cosine_similarity(query_vector, vector)
        results.append((score, text))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_k]

# ---------------- SESSION MEMORY ----------------

search_history = []

# ---------------- CLI MENU ----------------

def show_menu():
    print("\n==============================")
    print(" Semantic Search System ")
    print("==============================")
    print("1. Search documents")
    print("2. View search history")
    print("3. Exit")
    print("==============================")

while True:
    show_menu()
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        query = input("\n🔍 Enter your search query: ").strip()

        try:
            top_k = int(input("📊 Enter number of results to display: ").strip())
        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        search_history.append(query)

        results = semantic_search(query, top_k)

        print("\n📄 Search Results:")
        for i, (score, text) in enumerate(results, start=1):
            print(f"{i}. {text}  (score: {score:.3f})")

        # -------- RAG-READY CONTEXT --------
        print("\n📌 Retrieved context (for RAG-based answer generation):")
        for _, text in results:
            print("-", text)

    elif choice == "2":
        print("\n🕘 Search History:")
        if not search_history:
            print("No searches performed yet.")
        else:
            for i, q in enumerate(search_history, start=1):
                print(f"{i}. {q}")

    elif choice == "3":
        print("\n👋 Exiting Semantic Search System. Goodbye!")
        break

    else:
        print("\n❌ Invalid choice. Please select 1, 2, or 3.")
