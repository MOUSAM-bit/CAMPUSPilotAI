from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever