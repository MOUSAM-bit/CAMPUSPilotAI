from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(chunks, embeddings)

    if not os.path.exists("vector_store"):
        os.makedirs("vector_store")

    vector_db.save_local("vector_store")

    print("Vector Database Created Successfully!")

    return vector_db