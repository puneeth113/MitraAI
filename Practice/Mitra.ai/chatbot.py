import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

# Vector database location
VECTOR_DB_PATH = "vectorstore"

# Load OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_qa_chain():

    # HuggingFace embeddings (384 dimension)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load vector database
    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    # Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # OpenRouter LLM
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        temperature=0,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    # QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    return qa_chain


def ask_question(question):

    qa_chain = get_qa_chain()

    response = qa_chain.run(question)

    return response