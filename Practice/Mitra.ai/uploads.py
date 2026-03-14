import os
import streamlit as st
import pandas as pd
from database import save_document

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vectorstore"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


def upload_page():

    st.title("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF / Excel / CSV / TXT",
        type=["pdf", "xlsx", "xls", "csv", "txt"]
    )

    if uploaded_file is not None:

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully!")

        # Save metadata
        save_document(uploaded_file.name)

        process_document(file_path)


def process_document(file_path):

    st.info("Processing document...")

    extension = file_path.split(".")[-1].lower()

    documents = []

    # ---------------- PDF ----------------
    if extension == "pdf":

        loader = PyPDFLoader(file_path)
        documents = loader.load()

    # ---------------- TXT ----------------
    elif extension == "txt":

        loader = TextLoader(file_path)
        documents = loader.load()

    # ---------------- CSV ----------------
    elif extension == "csv":

        df = pd.read_csv(file_path)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        for index, row in df.iterrows():
            text = " ".join([str(v) for v in row.values])

            documents.append(
                Document(
                    page_content=text,
                    metadata={"row": index}
                )
            )

    # ---------------- Excel ----------------
    elif extension in ["xlsx", "xls"]:

        df = pd.read_excel(file_path)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        for index, row in df.iterrows():
            text = " ".join([str(v) for v in row.values])

            documents.append(
                Document(
                    page_content=text,
                    metadata={"row": index}
                )
            )

    else:
        st.error("Unsupported file format")
        return

    # ---------------- Chunking ----------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    # ---------------- Embeddings ----------------

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    vector_db.persist()

    st.success("Document added to knowledge base!")