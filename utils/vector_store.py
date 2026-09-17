from pathlib import Path

from langchain_chroma import Chroma


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# ChromaDB location
VECTOR_DB_PATH = BASE_DIR / "vector_db"


def create_vector_store(chunks, embeddings):

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_PATH),
        collection_name="student_documents"
    )

    return vector_store


def load_vector_store(embeddings):

    vector_store = Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        collection_name="student_documents",
        embedding_function=embeddings
    )

    return vector_store