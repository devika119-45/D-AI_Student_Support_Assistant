from utils.rag import ask_rag


def rag_tool(question):
    """
    Tool used by the AI Agent to answer
    questions from uploaded study materials.
    """

    return ask_rag(question)