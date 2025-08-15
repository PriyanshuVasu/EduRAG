from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

WIKIPEDIA_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Deep_learning"
]
DB_PATH = "./chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def main():
    """
    Ingests data from Wikipedia URLs, processes it, and stores it in a ChromaDB vector store.
    """
    print("--- Starting Data Ingestion from Wikipedia ---")

    print(f"Loading documents from {len(WIKIPEDIA_URLS)} URLs...")
    loader = WebBaseLoader(WIKIPEDIA_URLS)
    documents = loader.load()
    print(f"✅ Documents loaded successfully.")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Documents split into {len(chunks)} chunks.")

    print("Initializing embedding model...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", transport="rest")
    print("✅ Embedding model initialized.")

    print(f"Creating and persisting vector store at: {DB_PATH}...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print("✅ Vector store created and persisted.")

    print("\n--- Data Ingestion Complete ---")

if __name__ == "__main__":
    main()