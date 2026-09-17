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
# GEMINI MODEL
# =========================================================

def get_gemini_model():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY not found. "
            "Please check your .env file."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        api_key=api_key
    )


# =========================================================
# SAFE GEMINI CALL
# =========================================================

def call_gemini(prompt):

    llm = get_gemini_model()

    try:

        response = llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):

            return content

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

            return "\n".join(parts)

        return str(content)

    except Exception as e:

        error_text = str(e)

        if (
            "RESOURCE_EXHAUSTED" in error_text
            or "429" in error_text
            or "quota" in error_text.lower()
        ):

            raise RuntimeError(
                "⚠️ Gemini API quota has been exhausted.\n\n"
                "Your application is working correctly, "
                "but the Gemini API free-tier quota has "
                "been reached.\n\n"
                "Please wait for the quota to reset or "
                "enable a higher API quota/billing tier."
            )

        raise RuntimeError(
            f"Gemini API error: {error_text}"
        )