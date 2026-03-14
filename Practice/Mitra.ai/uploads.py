import streamlit as st
import os
import hashlib

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vectorstore"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


def file_hash(file):
    """Create hash to detect duplicate files"""
    file_bytes = file.getvalue()
    return hashlib.md5(file_bytes).hexdigest()


def upload_page():

    st.title("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt"]
    )

    if uploaded_file is None:
        return

    # Save file locally
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully")

    # Detect duplicates
    current_hash = file_hash(uploaded_file)

    hash_file = os.path.join(UPLOAD_DIR, uploaded_file.name + ".hash")

    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            old_hash = f.read()

        if old_hash == current_hash:
            st.warning("This document was already uploaded earlier.")
            return

    with open(hash_file, "w") as f:
        f.write(current_hash)

    # Load document
    if uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()

    # Extract preview text
    preview_text = documents[0].page_content

    st.subheader("Document Preview")

    st.text_area(
        "Preview (first page)",
        preview_text[:1000],
        height=300
    )

    st.info("Please confirm before adding to the knowledge base.")

    if st.button("Confirm and Process Document"):

        with st.spinner("Processing document..."):

            # Split text
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(documents)

            st.write(f"Total chunks created: {len(chunks)}")

            # Show sample chunk
            st.subheader("Chunk Preview")

            st.text_area(
                "First Chunk",
                chunks[0].page_content[:500],
                height=200
            )

            # Embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            vectordb = Chroma(
                persist_directory=VECTOR_DB_DIR,
                embedding_function=embeddings
            )

            vectordb.add_documents(chunks)

            vectordb.persist()

        st.success("Document successfully added to the knowledge base.")
