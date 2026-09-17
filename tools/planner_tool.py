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
# GENERATE STUDY PLAN
# =========================================================

def generate_study_plan(
    study_text,
    study_days,
    hours_per_day
):

    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )


    # -----------------------------------------------------
    # VALIDATE INPUT
    # -----------------------------------------------------

    if not study_text or not study_text.strip():

        raise ValueError(
            "Study material is empty."
        )


    if study_days < 1:

        raise ValueError(
            "Study days must be at least 1."
        )


    if hours_per_day < 1:

        raise ValueError(
            "Study hours must be at least 1."
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
    # LIMIT STUDY MATERIAL
    # -----------------------------------------------------

    study_text = study_text[:30000]


    # -----------------------------------------------------
    # STUDY PLAN PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an AI Study Planner for a college student.

Create a SHORT, SIMPLE and PRACTICAL study plan.

Study Days:
{study_days}

Study Hours Per Day:
{hours_per_day}

IMPORTANT RULES:

1. Use ONLY the provided study material.
2. Create exactly {study_days} days.
3. Maximum 3 topics per day.
4. Maximum 3 tasks per day.
5. Tasks must be short and actionable.
6. Include revision every day.
7. Do not write explanations.
8. Do not write paragraphs.
9. Do not repeat large parts of the study material.
10. Do not invent topics that are not present in the material.
11. Keep the plan realistic for {hours_per_day} hours per day.
12. Day numbers must start from 1 and continue sequentially.
13. Return ONLY valid JSON.
14. Do NOT use Markdown.
15. Do NOT use ```json.

Return exactly this format:

[
  {{
    "day": 1,
    "topics": [
      "Topic 1",
      "Topic 2"
    ],
    "tasks": [
      "Learn the main concepts",
      "Make short notes",
      "Revise for 15 minutes"
    ]
  }}
]

Create exactly {study_days} objects.

Study Material:
{study_text}
"""


    # -----------------------------------------------------
    # CALL GEMINI
    # -----------------------------------------------------

    try:

        response = llm.invoke(prompt)

    except Exception as e:

        raise RuntimeError(
            f"Study Planner AI error: {str(e)}"
        )


    # -----------------------------------------------------
    # GET RESPONSE CONTENT
    # -----------------------------------------------------

    content = response.content


    # -----------------------------------------------------
    # HANDLE GEMINI CONTENT
    # -----------------------------------------------------

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                parts.append(item)


        content = "".join(parts)


    else:

        content = str(content)


    # -----------------------------------------------------
    # CLEAN RESPONSE
    # -----------------------------------------------------

    content = content.strip()


    # Remove Markdown code fences if Gemini returns them

    if content.startswith("```json"):

        content = content[len("```json"):]


    elif content.startswith("```"):

        content = content[len("```"):]


    if content.endswith("```"):

        content = content[:-3]


    content = content.strip()


    # -----------------------------------------------------
    # FIND JSON ARRAY
    # -----------------------------------------------------

    start_index = content.find("[")

    end_index = content.rfind("]")


    if start_index == -1 or end_index == -1:

        raise ValueError(
            "AI did not return a valid JSON study plan."
        )


    content = content[
        start_index:end_index + 1
    ]


    # -----------------------------------------------------
    # PARSE JSON
    # -----------------------------------------------------

    try:

        plan = json.loads(content)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid study plan JSON: {e}"
        )


    # -----------------------------------------------------
    # VALIDATE PLAN
    # -----------------------------------------------------

    if not isinstance(plan, list):

        raise ValueError(
            "Study plan must be a list."
        )


    if len(plan) != study_days:

        raise ValueError(
            f"AI returned {len(plan)} days, "
            f"but {study_days} days were requested."
        )


    # -----------------------------------------------------
    # NORMALIZE PLAN
    # -----------------------------------------------------

    cleaned_plan = []


    for index, day_plan in enumerate(plan):

        if not isinstance(day_plan, dict):

            continue


        day_number = day_plan.get(
            "day",
            index + 1
        )


        topics = day_plan.get(
            "topics",
            []
        )


        tasks = day_plan.get(
            "tasks",
            []
        )


        # ---------------------------------------------
        # MAKE SURE TOPICS ARE LIST
        # ---------------------------------------------

        if not isinstance(topics, list):

            topics = [str(topics)]


        # Maximum 3 topics

        topics = [
            str(topic).strip()
            for topic in topics[:3]
            if str(topic).strip()
        ]


        # ---------------------------------------------
        # MAKE SURE TASKS ARE LIST
        # ---------------------------------------------

        if not isinstance(tasks, list):

            tasks = [str(tasks)]


        # Maximum 3 tasks

        tasks = [
            str(task).strip()
            for task in tasks[:3]
            if str(task).strip()
        ]


        # ---------------------------------------------
        # ALWAYS ADD REVISION
        # ---------------------------------------------

        revision_exists = any(
            "revis" in task.lower()
            for task in tasks
        )


        if not revision_exists:

            if len(tasks) >= 3:

                tasks[-1] = (
                    "Revise the day's topics for 15 minutes"
                )

            else:

                tasks.append(
                    "Revise the day's topics for 15 minutes"
                )


        # ---------------------------------------------
        # CREATE CLEAN DAY
        # ---------------------------------------------

        cleaned_plan.append(
            {
                "day": index + 1,
                "topics": topics,
                "tasks": tasks
            }
        )


    # -----------------------------------------------------
    # FINAL VALIDATION
    # -----------------------------------------------------

    if len(cleaned_plan) != study_days:

        raise ValueError(
            "Could not create a valid study plan."
        )


    return cleaned_plan