from rag.retriever import get_retriever

retriever = None


def retrieve_context(question):
    global retriever

    if retriever is None:
        retriever = get_retriever()

    docs = retriever.invoke(question)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n\n"

    return context