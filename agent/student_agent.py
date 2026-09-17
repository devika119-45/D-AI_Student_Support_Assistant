import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from tools.rag_tool import rag_tool


# =========================================================
# PROJECT ROOT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE
)


# =========================================================
# RAG TOOL
# =========================================================

@tool
def study_material_tool(question: str) -> str:
    """
    Search the uploaded study material and answer
    the student's question using the relevant content.
    """

    return rag_tool(question)


# =========================================================
# CREATE STUDENT AGENT
# =========================================================

def create_student_agent():

    # -----------------------------------------------------
    # GET API KEY
    # -----------------------------------------------------

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )


    # -----------------------------------------------------
    # GEMINI MODEL
    # -----------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        api_key=api_key
    )


    # -----------------------------------------------------
    # CONNECT ONLY RAG TOOL
    # -----------------------------------------------------

    llm_with_tools = llm.bind_tools(
        [
            study_material_tool
        ]
    )


    return llm_with_tools