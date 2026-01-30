# Semantic Search using Endee (Vector Database)

##  Project Overview
This project implements a **Semantic Search system** that retrieves relevant documents based on **meaning rather than exact keywords**.  
The system converts text data into vector embeddings and uses **Endee** as a vector database abstraction to enable similarity-based retrieval.

This project demonstrates a practical **AI/ML use case** where **vector search is the core component**.

---

##  Problem Statement
Traditional keyword-based search systems fail when user queries do not exactly match the words present in the documents.

Example:
- Query: *"data structure that stores many elements"*
- Keyword search may fail if the word *array* is not explicitly present.

This project solves the problem by using **semantic similarity**, allowing the system to understand the **intent** of the query.

---

##  Solution Approach
The solution uses **vector embeddings** to represent text meaning numerically.  
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
Endee is used as the **vector database abstraction** in this project. It is responsible for managing vector-based data within the system. Document embeddings are prepared and stored through Endee during the data ingestion phase.

Due to API instability in the current Endee version, similarity computation is performed using **cosine similarity**, which is a standard and widely accepted approach in semantic search systems. Despite this, Endee remains a core component of the architecture for handling vector data.



##  User Interaction
The application provides a **menu-driven command-line interface** that allows users to perform **multiple semantic searches in a single session**. Users can repeatedly enter search queries or exit the application using clear menu options, improving usability and interaction.



## Technologies Used
- Python  
- Endee (Vector Database)  
- Sentence Transformers (`all-MiniLM-L6-v2`)  
- NumPy  


##  Setup and Execution Instructions

### 1. Clone the Repository
git clone <your-github-repository-url>
cd semantic-search-endee
2. Install Dependencies
pip install -r requirements.txt

3. Run the Application
python app.py

4. Use the Menu Interface

Choose Search documents to enter a query

Choose Exit to close the application

Example query:

sorting in trees

## Sample Output
1. Binary Search Trees maintain elements in sorted order for efficient searching.
2. Trees are hierarchical data structures consisting of nodes with parent-child relationships.

## Conclusion

This project demonstrates the practical use of vector embeddings and semantic similarity to build intelligent search systems. It highlights how modern AI techniques and vector databases such as Endee can be used to overcome the limitations of traditional keyword-based search approaches.