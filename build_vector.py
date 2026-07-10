from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import create_vector_store

print("Loading documents...")
documents = load_documents()

print("Splitting documents...")
chunks = split_documents(documents)

print("Creating vector database...")
create_vector_store(chunks)

print("✅ Vector Database Created Successfully!")