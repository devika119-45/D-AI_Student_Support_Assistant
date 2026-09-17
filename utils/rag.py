import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from utils.vector_store import load_vector_store


# =========================================================
# PROJECT ROOT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# LOAD .ENV
# =========================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE
)


# =========================================================
# EMBEDDING MODEL
# =========================================================

def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


# =========================================================
# RAG QUESTION ANSWERING
# =========================================================

def ask_rag(question):

    # -----------------------------------------------------
    # Get API key
    # -----------------------------------------------------

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )


    # -----------------------------------------------------
    # Load embeddings
    # -----------------------------------------------------

    embeddings = get_embeddings()


    # -----------------------------------------------------
    # Load ChromaDB
    # -----------------------------------------------------

    vector_store = load_vector_store(
        embeddings
    )


    # -----------------------------------------------------
    # Search relevant PDF chunks
    # -----------------------------------------------------

    documents = vector_store.similarity_search(
        question,
        k=4
    )


    # -----------------------------------------------------
    # Check retrieved documents
    # -----------------------------------------------------

    if not documents:

        return (
            "I couldn't find relevant information "
            "in the uploaded study material."
        )


    # -----------------------------------------------------
    # Combine retrieved chunks
    # -----------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        api_key=api_key
    )


    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are an AI Student Support Assistant.

Answer the student's question using the provided
study material.

Study Material:
-------------------------
{context}
-------------------------

Student Question:
{question}

Instructions:

1. Answer clearly.
2. Use simple student-friendly language.
3. Use the study material as the primary source.
4. Do not invent information.
5. If the answer is not present in the study material,
say that it was not found in the uploaded material.
"""


    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------

    response = llm.invoke(prompt)


    # -----------------------------------------------------
    # Handle Gemini response format
    # -----------------------------------------------------

    if isinstance(response.content, str):

        return response.content


    if isinstance(response.content, list):

        text_parts = []

        for item in response.content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                text_parts.append(item)


        return "\n".join(
            text_parts
        )


    return str(response.content)