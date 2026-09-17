import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# STUDY PLAN GENERATOR
# =========================================================

def generate_study_plan(
    study_text,
    study_days,
    hours_per_day
):

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
You are an AI Study Planner for college students.

Create a personalized study plan using ONLY the
provided study material.

Student has:

Number of study days: {study_days}

Study hours per day: {hours_per_day}

Study Material:

{study_text}

Create a practical day-by-day study plan.

For every day include:

Day number
Topics to study
Approximate study time
Revision activity
Practice activity

At the end include:

1. Revision strategy
2. Important topics
3. Final preparation tips

Keep the plan simple and realistic.
Do not include topics that are not present
in the provided study material.
"""

    # -----------------------------------------------------
    # CALL GEMINI
    # -----------------------------------------------------

    response = llm.invoke(prompt)

    # -----------------------------------------------------
    # RETURN RESPONSE
    # -----------------------------------------------------

    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):

        parts = []

        for item in response.content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                parts.append(item)

        return "\n".join(parts)

    return str(response.content)