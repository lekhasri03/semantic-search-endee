import streamlit as st
from PyPDF2 import PdfReader
from utils.semantic_core import embed_documents, semantic_search
import re

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Semantic Search System",
    layout="wide"
)

st.title(" Semantic Search System")
st.caption(
    "Upload PDFs and retrieve the most relevant information using semantic similarity."
)

# ---------------- HELPER FUNCTIONS ----------------

def clean_page_text(text):
    lines = text.split("\n")
    cleaned_lines = []

    noise_keywords = [
        "GATE", "LAST MINUTE", "REVISION",
        "Notes", "Pg.", "Page", "Chapter", "CH."
    ]

    for line in lines:
        line = line.strip()

        # remove very short lines (page numbers, headers)
        if len(line) < 40:
            continue

        # remove noisy lines
        if any(word.lower() in line.lower() for word in noise_keywords):
            continue

        cleaned_lines.append(line)

    return " ".join(cleaned_lines)


def extract_complete_sentences(text, max_sentences=2):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 30]
    return ". ".join(sentences[:max_sentences]) + "."


def highlight_query(text, query):
    words = [w for w in query.split() if len(w) > 2]
    for word in words:
        text = re.sub(
            fr"(?i)\b({word})\b",
            r"<mark>\1</mark>",
            text
        )
    return text

# ---------------- SESSION STATE ----------------

if "documents" not in st.session_state:
    st.session_state.documents = []

if "embeddings" not in st.session_state:
    st.session_state.embeddings = []

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ----------------

st.sidebar.title(" Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    pages_text = []

    with st.spinner("Processing PDFs and indexing content..."):
        for pdf in uploaded_files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                raw_text = page.extract_text()
                if raw_text:
                    cleaned_text = clean_page_text(raw_text)
                    if cleaned_text:
                        pages_text.append(cleaned_text)

        st.session_state.documents = pages_text
        st.session_state.embeddings = embed_documents(pages_text)

    st.sidebar.success(
        f"PDFs processed successfully ({len(pages_text)} pages indexed)"
    )

# ---------------- SEARCH AREA ----------------

st.subheader(" Search Documents")

query = st.text_input("Enter your search query")

top_k = st.slider(
    "Number of relevant pages to retrieve",
    min_value=1,
    max_value=5,
    value=3
)

search_col, _ = st.columns([1, 5])
with search_col:
    search_clicked = st.button(" Search")

if search_clicked:
    if not st.session_state.documents:
        st.warning("Please upload PDF files first.")
    elif not query.strip():
        st.warning("Please enter a query.")
    else:
        st.session_state.history.append(query)

        results = semantic_search(
            query,
            st.session_state.documents,
            st.session_state.embeddings,
            top_k
        )

        # ---------------- SEARCH RESULTS ----------------

        st.markdown("###  Search Results (Semantic Matches)")

        for i, (score, doc) in enumerate(results, start=1):
            clean_text = extract_complete_sentences(doc, max_sentences=2)
            highlighted_text = highlight_query(clean_text, query)

            st.markdown(
                f"""
                <div style="
                    padding:16px;
                    border-radius:10px;
                    background-color:#1e1e1e;
                    margin-bottom:12px;
                ">
                    <b>{i}. Similarity Score:</b> {score:.3f}<br><br>
                    {highlighted_text}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---------------- SUMMARY ----------------

        st.markdown("###  Summary of Retrieved Information")

        combined_text = " ".join([doc for _, doc in results])
        summary_text = extract_complete_sentences(
            combined_text, max_sentences=4
        )
        summary_text = highlight_query(summary_text, query)

        st.markdown(
            f"""
            <div style="
                padding:18px;
                border-radius:10px;
                background-color:#0f172a;
                border:1px solid #334155;
            ">
                {summary_text}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- HISTORY ----------------

st.sidebar.subheader(" Search History")

if st.session_state.history:
    for q in st.session_state.history:
        st.sidebar.write(f"- {q}")
else:
    st.sidebar.write("No searches yet")

# ---------------- RESET ----------------

if st.sidebar.button("🔄 Reset Session"):
    st.session_state.clear()
    st.experimental_rerun()
