import streamlit as st

from utils.document_loader import extract_text_from_pdf
from utils.text_chunker import split_text_into_chunks
from utils.embedding import create_embedding_model
from utils.vector_store import create_vector_store

from agent.agent_runner import run_student_agent

from utils.session_manager import (
    initialize_session,
    set_document,
    clear_document,
    document_exists
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Student Support Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# SESSION INITIALIZATION
# =========================================================

initialize_session()


# =========================================================
# EXTRA SESSION STATE SAFETY
# =========================================================
# These make sure the app does not crash if any of these
# variables were not created inside session_manager.py.
# =========================================================

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

if "quiz_answer_submitted" not in st.session_state:
    st.session_state.quiz_answer_submitted = False

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []

if "study_plan" not in st.session_state:
    st.session_state.study_plan = None

if "study_plan_days" not in st.session_state:
    st.session_state.study_plan_days = None

if "study_plan_hours" not in st.session_state:
    st.session_state.study_plan_hours = None


# =========================================================
# MAIN TITLE
# =========================================================

st.title("🎓 AI Student Support Assistant")

st.write(
    "Your intelligent academic assistant powered by Agentic AI."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Student Menu")

    option = st.radio(
        "Choose an option:",
        [
            "📄 Study Materials",
            "💬 AI Assistant",
            "📝 Quiz",
            "📅 Study Planner",
            "📊 Progress"
        ],
        key="main_navigation"
    )

    st.divider()

    # -----------------------------------------------------
    # ACTIVE PDF STATUS
    # -----------------------------------------------------

    st.subheader("📄 Current Study Material")

    if document_exists():

        st.success(
            f"Active PDF:\n\n"
            f"**{st.session_state.uploaded_file_name}**"
        )

        st.caption(
            "This PDF is available across all sections "
            "until you close it."
        )

        if st.button(
            "❌ Close PDF",
            use_container_width=True,
            key="sidebar_close_pdf"
        ):

            clear_document()

            # Clear quiz because it belongs to old PDF
            st.session_state.quiz_result = None
            st.session_state.quiz_score = None
            st.session_state.quiz_current_question = 0
            st.session_state.quiz_answers = []
            st.session_state.quiz_answer_submitted = False

            # Clear study plan
            st.session_state.study_plan = None
            st.session_state.study_plan_days = None
            st.session_state.study_plan_hours = None

            # Clear AI conversation
            st.session_state.ai_chat_history = []

            st.success(
                "PDF closed successfully."
            )

            st.rerun()

    else:

        st.info(
            "📄 No PDF uploaded yet."
        )

    st.divider()

    st.info(
        "🎓 AI Student Support Assistant helps students "
        "study, understand notes, generate quizzes and "
        "create personalized study plans."
    )


# =========================================================
# AI ASSISTANT
# =========================================================

if option == "💬 AI Assistant":

    st.header("💬 AI Student Assistant")

    st.write(
        "Ask your questions about the uploaded study "
        "material and let the AI Agent help you."
    )

    st.divider()

    # -----------------------------------------------------
    # CHECK PDF
    # -----------------------------------------------------

    if not document_exists():

        st.warning(
            "📄 Please upload a study PDF first."
        )

        st.info(
            "Go to **📄 Study Materials** and upload "
            "your PDF."
        )

    else:

        st.success(
            f"📄 Using: "
            f"**{st.session_state.uploaded_file_name}**"
        )

        st.divider()

        # -------------------------------------------------
        # PREVIOUS QUESTIONS / ANSWERS
        # -------------------------------------------------

        if st.session_state.ai_chat_history:

            st.subheader("💬 Previous Questions")

            for index, chat in enumerate(
                st.session_state.ai_chat_history
            ):

                with st.expander(
                    f"Question {index + 1}: {chat['question']}"
                ):

                    st.markdown(
                        "**🤖 AI Answer:**"
                    )

                    st.write(
                        chat["answer"]
                    )

        # -------------------------------------------------
        # NEW QUESTION
        # -------------------------------------------------

        st.subheader("➕ Ask a New Question")

        user_question = st.text_input(
            "Ask your question:",
            placeholder=(
                "Example: Explain supervised learning."
            ),
            key="ai_question_input"
        )

        col1, col2 = st.columns(2)

        with col1:

            ask_button = st.button(
                "🤖 Ask AI",
                use_container_width=True,
                key="ask_ai_button"
            )

        with col2:

            clear_chat_button = st.button(
                "🗑️ Clear Questions",
                use_container_width=True,
                key="clear_ai_history_button"
            )

        # -------------------------------------------------
        # CLEAR CHAT
        # -------------------------------------------------

        if clear_chat_button:

            st.session_state.ai_chat_history = []

            st.rerun()

        # -------------------------------------------------
        # ASK AI
        # -------------------------------------------------

        if ask_button:

            if user_question.strip():

                try:

                    with st.spinner(
                        "🤖 AI Agent is thinking..."
                    ):

                        answer = run_student_agent(
                            user_question
                        )

                    # Save question and answer
                    st.session_state.ai_chat_history.append(
                        {
                            "question": user_question,
                            "answer": answer
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Error: {str(e)}"
                    )

            else:

                st.warning(
                    "⚠️ Please enter a question."
                )


# =========================================================
# STUDY MATERIALS
# =========================================================

elif option == "📄 Study Materials":

    st.header("📄 Study Materials")

    st.write(
        "Upload your study PDF. Once uploaded, the "
        "document remains available across the entire "
        "application until you close it."
    )

    st.divider()

    # -----------------------------------------------------
    # CURRENT PDF
    # -----------------------------------------------------

    if document_exists():

        st.success(
            f"📄 Currently active: "
            f"**{st.session_state.uploaded_file_name}**"
        )

        st.info(
            "✅ This PDF is already loaded. "
            "You don't need to upload it again when "
            "changing sections."
        )

        st.divider()

        # -------------------------------------------------
        # EXTRACTED TEXT
        # -------------------------------------------------

        st.subheader("📄 Current PDF Content")

        st.text_area(
            "Extracted Text",
            st.session_state.extracted_text,
            height=300,
            key="current_pdf_text"
        )

        # -------------------------------------------------
        # CHUNKS
        # -------------------------------------------------

        st.subheader("✂️ Document Chunks")

        chunks = st.session_state.chunks

        st.write(
            f"Total chunks: **{len(chunks)}**"
        )

        for i, chunk in enumerate(chunks):

            with st.expander(
                f"Chunk {i + 1}"
            ):

                st.write(chunk)

        st.divider()

        st.warning(
            "⚠️ Uploading another PDF will replace the "
            "current active PDF."
        )

    else:

        # -------------------------------------------------
        # PDF UPLOAD
        # -------------------------------------------------

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            key="main_pdf_uploader"
        )

        if uploaded_file:

            st.success(
                f"✅ Uploaded successfully: "
                f"{uploaded_file.name}"
            )

            # -------------------------------------------------
            # TEXT EXTRACTION
            # -------------------------------------------------

            with st.spinner(
                "📖 Extracting text from PDF..."
            ):

                extracted_text = extract_text_from_pdf(
                    uploaded_file
                )

            if extracted_text:

                st.success(
                    "✅ Text extracted successfully!"
                )

                # -------------------------------------------------
                # TEXT CHUNKING
                # -------------------------------------------------

                with st.spinner(
                    "✂️ Splitting document into chunks..."
                ):

                    chunks = split_text_into_chunks(
                        extracted_text
                    )

                st.success(
                    f"✅ Document divided into "
                    f"{len(chunks)} chunks."
                )

                # -------------------------------------------------
                # EMBEDDINGS
                # -------------------------------------------------

                with st.spinner(
                    "🧠 Creating embeddings..."
                ):

                    embeddings = create_embedding_model()

                st.success(
                    "✅ Embedding model loaded successfully!"
                )

                # -------------------------------------------------
                # CHROMADB
                # -------------------------------------------------

                with st.spinner(
                    "🗄️ Storing document in ChromaDB..."
                ):

                    create_vector_store(
                        chunks,
                        embeddings
                    )

                st.success(
                    "✅ Document stored successfully "
                    "in ChromaDB!"
                )

                # -------------------------------------------------
                # SAVE DOCUMENT
                # -------------------------------------------------

                set_document(
                    uploaded_file.name,
                    extracted_text,
                    chunks
                )

                # -------------------------------------------------
                # RESET MODULES FOR NEW PDF
                # -------------------------------------------------

                st.session_state.quiz_result = None
                st.session_state.quiz_score = None
                st.session_state.quiz_current_question = 0
                st.session_state.quiz_answers = []
                st.session_state.quiz_answer_submitted = False

                st.session_state.study_plan = None
                st.session_state.study_plan_days = None
                st.session_state.study_plan_hours = None

                st.session_state.ai_chat_history = []

                st.success(
                    "📌 PDF is now active across the "
                    "entire application."
                )

                st.info(
                    "You can now open AI Assistant, Quiz, "
                    "Study Planner or Progress without "
                    "uploading the PDF again."
                )

                st.rerun()

            else:

                st.warning(
                    "⚠️ No readable text found in this PDF."
                )


# =========================================================
# QUIZ
# =========================================================

elif option == "📝 Quiz":

    st.header("📝 AI Quiz")

    st.write(
        "Test your knowledge from your uploaded "
        "study material."
    )

    st.divider()

    # -----------------------------------------------------
    # CHECK DOCUMENT
    # -----------------------------------------------------

    if not document_exists():

        st.warning(
            "📄 Please upload a study PDF first."
        )

        st.info(
            "Go to **📄 Study Materials** and upload "
            "your study material."
        )

    # -----------------------------------------------------
    # QUIZ NOT GENERATED
    # -----------------------------------------------------

    elif not st.session_state.quiz_result:

        st.subheader(
            "⚙️ Create Your Quiz"
        )

        col1, col2 = st.columns(2)

        with col1:

            number_of_questions = st.selectbox(
                "Number of Questions",
                [5, 10, 15, 20],
                index=0,
                key="quiz_number_questions"
            )

        with col2:

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ],
                index=1,
                key="quiz_difficulty"
            )

        st.divider()

        st.info(
            "💡 Questions will be generated only "
            "from your uploaded study material."
        )

        if st.button(
            "🚀 Start Quiz",
            use_container_width=True,
            key="start_quiz_button"
        ):

            try:

                from tools.quiz_tool import generate_quiz

                with st.spinner(
                    "🤖 Preparing your quiz..."
                ):

                    quiz = generate_quiz(
                        study_text=(
                            st.session_state.extracted_text
                        ),
                        number_of_questions=(
                            number_of_questions
                        ),
                        difficulty=difficulty
                    )

                if not quiz:

                    st.error(
                        "❌ Quiz could not be generated."
                    )

                else:

                    # Save quiz
                    st.session_state.quiz_result = quiz

                    # Reset current quiz
                    st.session_state.quiz_score = None

                    st.session_state.quiz_current_question = 0

                    st.session_state.quiz_answers = []

                    st.session_state.quiz_answer_submitted = False

                    # IMPORTANT:
                    # Do NOT reset quiz_attempts here
                    if "quiz_attempts" not in st.session_state:

                        st.session_state.quiz_attempts = 0

                    st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Quiz generation error: {str(e)}"
                )

    # -----------------------------------------------------
    # QUIZ EXISTS
    # -----------------------------------------------------

    else:

        quiz = st.session_state.quiz_result

        # -------------------------------------------------
        # SAFETY
        # -------------------------------------------------

        if "quiz_current_question" not in st.session_state:

            st.session_state.quiz_current_question = 0

        if "quiz_answers" not in st.session_state:

            st.session_state.quiz_answers = []

        if "quiz_answer_submitted" not in st.session_state:

            st.session_state.quiz_answer_submitted = False

        if "quiz_score" not in st.session_state:

            st.session_state.quiz_score = None

        if "quiz_attempts" not in st.session_state:

            st.session_state.quiz_attempts = 0

        current_index = (
            st.session_state.quiz_current_question
        )

        total_questions = len(quiz)

        # -------------------------------------------------
        # QUIZ COMPLETED
        # -------------------------------------------------

        if current_index >= total_questions:

            st.subheader(
                "🎉 Quiz Completed!"
            )

            score = st.session_state.quiz_score

            if score is not None:

                st.metric(
                    "Your Score",
                    f"{score}%"
                )

                st.progress(
                    score / 100
                )

            # -------------------------------------------------
            # PERFORMANCE
            # -------------------------------------------------

            if score >= 80:

                st.success(
                    "🏆 Excellent! You have a strong "
                    "understanding of the material."
                )

            elif score >= 50:

                st.warning(
                    "👍 Good job! Review the questions "
                    "you missed."
                )

            else:

                st.error(
                    "📚 Keep practicing. Review your "
                    "study material and try again."
                )

            st.divider()

            # -------------------------------------------------
            # ANSWER REVIEW
            # -------------------------------------------------

            st.subheader(
                "📖 Answer Review"
            )

            for index, question in enumerate(quiz):

                if index < len(
                    st.session_state.quiz_answers
                ):

                    user_answer = (
                        st.session_state.quiz_answers[index]
                    )

                else:

                    user_answer = None

                correct_answer = (
                    question["answer"].upper()
                )

                if user_answer == correct_answer:

                    st.success(
                        f"Question {index + 1}: "
                        f"Correct ✅"
                    )

                else:

                    st.error(
                        f"Question {index + 1}: "
                        f"Incorrect ❌"
                    )

                st.write(
                    f"Correct Answer: "
                    f"**{correct_answer}**"
                )

                st.caption(
                    question.get(
                        "explanation",
                        ""
                    )
                )

            st.divider()

            # -------------------------------------------------
            # NEW QUIZ
            # -------------------------------------------------

            if st.button(
                "🔄 Start New Quiz",
                use_container_width=True,
                key="start_new_quiz_button"
            ):

                st.session_state.quiz_result = None

                st.session_state.quiz_score = None

                st.session_state.quiz_current_question = 0

                st.session_state.quiz_answers = []

                st.session_state.quiz_answer_submitted = False

                st.rerun()

        # -------------------------------------------------
        # CURRENT QUESTION
        # -------------------------------------------------

        else:

            question = quiz[current_index]

            # -------------------------------------------------
            # QUESTION HEADER
            # -------------------------------------------------

            st.markdown(
                f"### 📝 Question "
                f"{current_index + 1} "
                f"of {total_questions}"
            )

            progress_value = (
                (current_index + 1)
                / total_questions
            )

            st.progress(
                progress_value
            )

            st.caption(
                f"Question {current_index + 1} "
                f"of {total_questions}"
            )

            st.divider()

            # -------------------------------------------------
            # QUESTION
            # -------------------------------------------------

            st.subheader(
                question["question"]
            )

            st.write("")

            options = question["options"]

            # -------------------------------------------------
            # OPTIONS
            # -------------------------------------------------

            selected_option = st.radio(
                "Select the correct answer:",
                [
                    f"A. {options['A']}",
                    f"B. {options['B']}",
                    f"C. {options['C']}",
                    f"D. {options['D']}"
                ],
                key=f"quiz_option_{current_index}"
            )

            st.write("")

            # =================================================
            # BEFORE SUBMIT
            # =================================================

            if not st.session_state.quiz_answer_submitted:

                if st.button(
                    "✅ Submit Answer",
                    use_container_width=True,
                    key=f"submit_answer_{current_index}"
                ):

                    selected_letter = (
                        selected_option[0]
                    )

                    # Save answer
                    st.session_state.quiz_answers.append(
                        selected_letter
                    )

                    # Mark answer as submitted
                    st.session_state.quiz_answer_submitted = True

                    st.rerun()

            # =================================================
            # AFTER SUBMIT
            # =================================================

            else:

                # Get saved answer
                user_answer = (
                    st.session_state.quiz_answers[
                        current_index
                    ]
                )

                correct_answer = (
                    question["answer"].upper()
                )

                # -------------------------------------------------
                # RESULT
                # -------------------------------------------------

                if user_answer == correct_answer:

                    st.success(
                        "🎉 Correct Answer!"
                    )

                else:

                    st.error(
                        "❌ Incorrect Answer"
                    )

                # -------------------------------------------------
                # CORRECT ANSWER
                # -------------------------------------------------

                st.info(
                    f"Correct Answer: "
                    f"**{correct_answer}**"
                )

                # -------------------------------------------------
                # EXPLANATION
                # -------------------------------------------------

                explanation = question.get(
                    "explanation",
                    "Review the study material for this topic."
                )

                st.caption(
                    explanation
                )

                st.divider()

                # =================================================
                # NEXT QUESTION
                # =================================================

                if current_index + 1 < total_questions:

                    if st.button(
                        "Next Question →",
                        use_container_width=True,
                        key=f"next_question_{current_index}"
                    ):

                        st.session_state.quiz_current_question += 1

                        st.session_state.quiz_answer_submitted = False

                        st.rerun()

                # =================================================
                # FINISH QUIZ
                # =================================================

                else:

                    if st.button(
                        "🏁 Finish Quiz",
                        use_container_width=True,
                        key="finish_quiz_button"
                    ):

                        correct_count = 0

                        for i, ans in enumerate(
                            st.session_state.quiz_answers
                        ):

                            if (
                                ans
                                == quiz[i]["answer"].upper()
                            ):

                                correct_count += 1

                        percentage = int(
                            (
                                correct_count
                                / total_questions
                            ) * 100
                        )

                        # Save score
                        st.session_state.quiz_score = (
                            percentage
                        )

                        # Increment attempt
                        st.session_state.quiz_attempts = (
                            st.session_state.get(
                                "quiz_attempts",
                                0
                            ) + 1
                        )

                        # Mark complete
                        st.session_state.quiz_current_question = (
                            total_questions
                        )

                        st.session_state.quiz_answer_submitted = (
                            False
                        )

                        st.rerun()


# =========================================================
# STUDY PLANNER
# =========================================================

elif option == "📅 Study Planner":

    st.header("📅 AI Study Planner")

    st.write(
        "Create a short and practical study plan "
        "from your uploaded material."
    )

    st.divider()

    # -----------------------------------------------------
    # CHECK DOCUMENT
    # -----------------------------------------------------

    if not document_exists():

        st.warning(
            "📄 Please upload a study PDF first."
        )

        st.info(
            "Go to **📄 Study Materials** and upload "
            "your study material."
        )

    else:

        st.success(
            f"📄 Planning based on: "
            f"**{st.session_state.uploaded_file_name}**"
        )

        st.divider()

        st.subheader(
            "📅 Create Your Study Plan"
        )

        col1, col2 = st.columns(2)

        with col1:

            study_days = st.selectbox(
                "Study duration",
                [1, 3, 5, 7, 14],
                index=3,
                key="study_days_input"
            )

        with col2:

            hours_per_day = st.selectbox(
                "Hours per day",
                [1, 2, 3, 4, 5],
                index=1,
                key="study_hours_input"
            )

        st.write("")

        if st.button(
            "📅 Create Short Study Plan",
            use_container_width=True,
            key="create_study_plan_button"
        ):

            try:

                # ---------------------------------------------
                # GET DOCUMENT CONTENT
                # ---------------------------------------------

                chunks = st.session_state.chunks

                if not chunks:

                    st.warning(
                        "⚠️ No study topics found."
                    )

                else:

                    # ---------------------------------------------
                    # SELECT IMPORTANT TOPICS
                    # ---------------------------------------------

                    max_topics = study_days * 2

                    topics = chunks[:max_topics]

                    # ---------------------------------------------
                    # CREATE SHORT PLAN
                    # ---------------------------------------------

                    plan = []

                    for day in range(study_days):

                        topic_index_1 = day * 2
                        topic_index_2 = day * 2 + 1

                        day_topics = []

                        if topic_index_1 < len(topics):

                            text1 = topics[
                                topic_index_1
                            ]

                            # Keep it short
                            short_text1 = (
                                text1[:180]
                                .replace("\n", " ")
                            )

                            day_topics.append(
                                short_text1
                            )

                        if topic_index_2 < len(topics):

                            text2 = topics[
                                topic_index_2
                            ]

                            short_text2 = (
                                text2[:180]
                                .replace("\n", " ")
                            )

                            day_topics.append(
                                short_text2
                            )

                        if not day_topics:

                            day_topics.append(
                                "Revise previous topics"
                            )

                        plan.append(
                            {
                                "day": day + 1,
                                "topics": day_topics
                            }
                        )

                    st.session_state.study_plan = plan

                    st.session_state.study_plan_days = (
                        study_days
                    )

                    st.session_state.study_plan_hours = (
                        hours_per_day
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Study plan error: {str(e)}"
                )

        # -----------------------------------------------------
        # SHOW PLAN
        # -----------------------------------------------------

        if st.session_state.study_plan:

            st.divider()

            st.subheader(
                "📋 Your Short Study Plan"
            )

            st.caption(
                f"{st.session_state.study_plan_days} days • "
                f"{st.session_state.study_plan_hours} "
                f"hour(s) per day"
            )

            for day_plan in (
                st.session_state.study_plan
            ):

                with st.container():

                    st.markdown(
                        f"### 📅 Day {day_plan['day']}"
                    )

                    for topic in day_plan["topics"]:

                        st.write(
                            f"☐ {topic}"
                        )

                    st.caption(
                        "🎯 Focus: Understand → Practice → Review"
                    )

            st.divider()

            st.success(
                "💡 Keep each session focused. "
                "Finish today's topics before moving "
                "to the next day."
            )

            if st.button(
                "🗑️ Remove Study Plan",
                use_container_width=True,
                key="remove_study_plan_button"
            ):

                st.session_state.study_plan = None

                st.rerun()


# =========================================================
# PROGRESS
# =========================================================

elif option == "📊 Progress":

    st.header("📊 Student Progress")

    st.write(
        "Track your study and quiz performance."
    )

    st.divider()

    # -----------------------------------------------------
    # PDF STATUS
    # -----------------------------------------------------

    if document_exists():

        st.success(
            f"📄 Active Material: "
            f"**{st.session_state.uploaded_file_name}**"
        )

    else:

        st.info(
            "📄 No active study material."
        )

    st.divider()

    # -----------------------------------------------------
    # QUIZ SCORE
    # -----------------------------------------------------

    quiz_score = st.session_state.get(
        "quiz_score",
        None
    )

    quiz_attempts = st.session_state.get(
        "quiz_attempts",
        0
    )

    # -----------------------------------------------------
    # STUDY PROGRESS
    # -----------------------------------------------------

    if document_exists():

        chunks = st.session_state.get(
            "chunks",
            []
        )

        if chunks:

            study_progress = min(
                100,
                len(chunks) * 5
            )

        else:

            study_progress = 0

    else:

        study_progress = 0

    # -----------------------------------------------------
    # COMPLETED TOPICS
    # -----------------------------------------------------

    completed_topics = 0

    if quiz_score is not None:

        completed_topics = (
            st.session_state.quiz_current_question
        )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Study Progress",
            f"{study_progress}%"
        )

    with col2:

        if quiz_score is not None:

            st.metric(
                "Quiz Score",
                f"{quiz_score}%"
            )

        else:

            st.metric(
                "Quiz Score",
                "Not attempted"
            )

    with col3:

        st.metric(
            "Completed Topics",
            completed_topics
        )

    st.divider()

    # -----------------------------------------------------
    # QUIZ DETAILS
    # -----------------------------------------------------

    st.subheader(
        "📝 Quiz Performance"
    )

    if quiz_score is not None:

        st.progress(
            quiz_score / 100
        )

        st.write(
            f"Latest Quiz Score: **{quiz_score}%**"
        )

        st.write(
            f"Quiz Attempts: **{quiz_attempts}**"
        )

        if quiz_score >= 80:

            st.success(
                "🏆 Excellent performance!"
            )

        elif quiz_score >= 50:

            st.warning(
                "👍 Good performance. "
                "Review the topics you missed."
            )

        else:

            st.error(
                "📚 More practice is recommended."
            )

    else:

        st.info(
            "📝 Complete a quiz to see your score."
        )

    st.divider()

    # -----------------------------------------------------
    # STUDY PLAN STATUS
    # -----------------------------------------------------

    st.subheader(
        "📅 Study Plan"
    )

    if st.session_state.study_plan:

        st.success(
            "✅ Study plan created."
        )

        st.write(
            f"Duration: "
            f"**{st.session_state.study_plan_days} days**"
        )

        st.write(
            f"Daily study time: "
            f"**{st.session_state.study_plan_hours} hour(s)**"
        )

    else:

        st.info(
            "📅 No study plan created yet."
        )

    st.divider()

    # -----------------------------------------------------
    # AI QUESTIONS
    # -----------------------------------------------------

    st.subheader(
        "💬 AI Assistant Activity"
    )

    total_ai_questions = len(
        st.session_state.ai_chat_history
    )

    st.metric(
        "Questions Asked",
        total_ai_questions
    )

    if total_ai_questions > 0:

        st.success(
            "✅ Your AI Assistant questions "
            "are saved during this session."
        )

    else:

        st.info(
            "No AI questions asked yet."
        )