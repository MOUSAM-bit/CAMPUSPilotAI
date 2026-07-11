from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

_embeddings = None


def get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings


def get_retriever():

    embeddings = get_embeddings()

    vector_db = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_db.as_retriever(
        search_kwargs={"k": 3}
    )