from rag.retriever import get_retriever

retriever = get_retriever()


def retrieve_context(question):

    docs = retriever.invoke(question)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n\n"

    return context