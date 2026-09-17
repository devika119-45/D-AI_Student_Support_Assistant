import os
import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# GENERATE QUIZ
# =========================================================

def generate_quiz(
    study_text,
    number_of_questions=5,
    difficulty="Medium"
):

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )


    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.3,
        api_key=api_key
    )


    # -----------------------------------------------------
    # LIMIT TEXT
    # -----------------------------------------------------

    study_text = study_text[:30000]


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an AI Quiz Generator for college students.

Create exactly {number_of_questions}
multiple-choice questions from the study material.

Difficulty: {difficulty}

IMPORTANT RULES:

1. Use ONLY the provided study material.
2. Do not use outside information.
3. Each question must have exactly 4 options.
4. Only one option must be correct.
5. Give the correct answer as A, B, C or D.
6. Give a short explanation.
7. Return ONLY valid JSON.
8. Do not use markdown.
9. Do not add ```json or ```.

Return exactly this structure:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A",
    "explanation": "Short explanation"
  }}
]

Study Material:

{study_text}
"""


    # -----------------------------------------------------
    # CALL GEMINI
    # -----------------------------------------------------

    response = llm.invoke(prompt)


    content = response.content


    # -----------------------------------------------------
    # EXTRACT TEXT
    # -----------------------------------------------------

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                text_parts.append(item)

        content = "".join(text_parts)


    else:

        content = str(content)


    # -----------------------------------------------------
    # CLEAN JSON
    # -----------------------------------------------------

    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()


    # -----------------------------------------------------
    # PARSE JSON
    # -----------------------------------------------------

    try:

        quiz_data = json.loads(content)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"AI returned invalid quiz JSON: {e}"
        )


    # -----------------------------------------------------
    # VALIDATE
    # -----------------------------------------------------

    if not isinstance(quiz_data, list):

        raise ValueError(
            "Quiz format is invalid."
        )


    if len(quiz_data) == 0:

        raise ValueError(
            "No quiz questions were generated."
        )


    return quiz_data