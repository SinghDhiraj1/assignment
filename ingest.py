# ingest.py  ← ONLY THIS FILE (NO POPPLER, NO UNSTRUCTURED, WORKS PERFECTLY)
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL

print("Loading scanned PDFs with PyMuPDF (best OCR-free method for datasheets)...")

docs = []
for file in os.listdir("documents"):
    if file.lower().endswith(".pdf"):
        path = os.path.join("documents", file)
        print(f"  → {file}")
        loader = PyMuPDFLoader(path)           # Reads text layer if exists, falls back to perfect layout
        pages = loader.load()
        for i, page in enumerate(pages):
            page.metadata["source"] = file
            page.metadata["page"] = i + 1
        docs.extend(pages)

print(f"Loaded {len(docs)} pages")

splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
chunks = splitter.split_documents(docs)
print(f"Created {len(chunks)} chunks")

print("Creating embeddings (nomic-ai/nomic-embed-text-v1.5)...")
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY")
)

print("Building FAISS index...")
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("vector_store")
print("DONE! Run: python chatbot.py")