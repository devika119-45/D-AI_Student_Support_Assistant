import streamlit as st


# =========================================================
# INITIALIZE SESSION
# =========================================================

def initialize_session():

    # -----------------------------------------------------
    # DOCUMENT
    # -----------------------------------------------------

    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None

    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = None

    if "chunks" not in st.session_state:
        st.session_state.chunks = []

    if "document_loaded" not in st.session_state:
        st.session_state.document_loaded = False


    # -----------------------------------------------------
    # AI ASSISTANT CHAT HISTORY
    # -----------------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    if "quiz_result" not in st.session_state:
        st.session_state.quiz_result = None

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = None

    if "quiz_attempts" not in st.session_state:
        st.session_state.quiz_attempts = 0

    if "quiz_current_question" not in st.session_state:
        st.session_state.quiz_current_question = 0

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False


    # -----------------------------------------------------
    # STUDY PLANNER
    # -----------------------------------------------------

    if "study_plan" not in st.session_state:
        st.session_state.study_plan = None


# =========================================================
# SET DOCUMENT
# =========================================================

def set_document(
    file_name,
    extracted_text,
    chunks
):

    st.session_state.uploaded_file_name = file_name

    st.session_state.extracted_text = extracted_text

    st.session_state.chunks = chunks

    st.session_state.document_loaded = True


# =========================================================
# CHECK DOCUMENT
# =========================================================

def document_exists():

    return (
        st.session_state.get(
            "document_loaded",
            False
        )
        and
        st.session_state.get(
            "extracted_text"
        ) is not None
    )


# =========================================================
# CLEAR DOCUMENT
# =========================================================

def clear_document():

    # -----------------------------------------------------
    # CLEAR PDF
    # -----------------------------------------------------

    st.session_state.uploaded_file_name = None

    st.session_state.extracted_text = None

    st.session_state.chunks = []

    st.session_state.document_loaded = False


    # -----------------------------------------------------
    # CLEAR AI CHAT
    # -----------------------------------------------------

    st.session_state.chat_history = []


    # -----------------------------------------------------
    # CLEAR QUIZ
    # -----------------------------------------------------

    st.session_state.quiz_result = None

    st.session_state.quiz_score = None

    st.session_state.quiz_current_question = 0

    st.session_state.quiz_answers = []

    st.session_state.quiz_submitted = False


    # -----------------------------------------------------
    # CLEAR STUDY PLAN
    # -----------------------------------------------------

    st.session_state.study_plan = None