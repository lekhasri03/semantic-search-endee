# Semantic Search using Endee (Vector Database)

##  Project Overview
This project implements a Semantic Search system that retrieves relevant documents based on meaning rather than exact keywords  
The system converts text data into vector embeddings and uses Endee as a vector database abstraction to enable similarity-based retrieval.

This project demonstrates a practical AI/ML use case where vector search is the core component

---

##  Problem Statement
Traditional keyword-based search systems fail when user queries do not exactly match the words present in the documents.

Example:
- Query: *"data structure that stores many elements"*
- Keyword search may fail if the word *array* is not explicitly present.

This project solves the problem by using semantic similarity, allowing the system to understand the intent of the query.

---

##  Solution Approach
The solution uses vector embeddings to represent text meaning numerically.  
Similarity between vectors is calculated to retrieve the most relevant documents.

### High-Level Workflow
1. Load text documents  
2. Convert documents into embeddings using a transformer-based model  
3. Store embeddings using Endee  
4. Convert user query into an embedding  
5. Perform similarity comparison  
6. Return the most relevant results  

---

## System Design / Architecture

The system follows a modular architecture where vector embeddings are the core component. Text documents are converted into numerical embeddings using a transformer-based model. These embeddings are handled using Endee as a vector database abstraction. When a user provides a search query, the query is converted into an embedding and compared with stored document embeddings using cosine similarity to retrieve the most relevant results.

Text Documents
↓
Sentence Transformer (Embeddings)
↓
Vector Embeddings
↓
Endee (Vector Database Abstraction)
↓
Cosine Similarity Search
↓
Relevant Documents




##  How Endee is Used
Endee is used as the vector database abstraction in this project. It is responsible for managing vector-based data within the system. Document embeddings are prepared and stored through Endee during the data ingestion phase.

Due to API instability in the current Endee version, similarity computation is performed using cosine similarity, which is a standard and widely accepted approach in semantic search systems. Despite this, Endee remains a core component of the architecture for handling vector data.



##  User Interaction
The system is designed to be easily extended into a Retrieval-Augmented Generation (RAG) pipeline. After performing semantic search, the retrieved top-k documents are displayed as contextual information. This context can be directly passed to a Large Language Model (LLM) to generate grounded, context-aware answers, enabling applications such as document question answering and knowledge assistants.



## Technologies Used
- Python  
- Endee (Vector Database)  
- Sentence Transformers (`all-MiniLM-L6-v2`)  
- NumPy  


##  Setup and Execution Instructions

### 1. Clone the Repository
git clone https://github.com/lekhasri03/semantic-search-endee
cd semantic-search-endee
2. Install Dependencies
pip install -r requirements.txt

3. Run the Application
python app.py

4. Use the Menu Interface

1. Search documents
2. View search history
3. Exit


Enter your choice: 1
 Enter your search query: sorting in trees
 Enter number of results to display: 3

Search Results:
1. Binary Search Trees maintain elements in sorted order...
2. Trees are hierarchical data structures...
3. Heaps are complete binary trees...

 Retrieved context (for RAG-based answer generation):
- Binary Search Trees maintain elements in sorted order...
- Trees are hierarchical data structures...
- Heaps are complete binary trees...

Enter your choice: 2
🕘 Search History:
1. sorting in trees


## Conclusion

This project demonstrates the practical use of vector embeddings and semantic similarity to build intelligent search systems. It highlights how modern AI techniques and vector databases such as Endee can be used to overcome the limitations of traditional keyword-based search approaches.