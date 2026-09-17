from agent.student_agent import (
    create_student_agent,
    study_material_tool
)


# =========================================================
# RUN STUDENT AGENT
# =========================================================

def run_student_agent(question):

    # -----------------------------------------------------
    # CREATE AGENT
    # -----------------------------------------------------

    agent = create_student_agent()


    # -----------------------------------------------------
    # SEND QUESTION TO AGENT
    # -----------------------------------------------------

    response = agent.invoke(
        question
    )


    # -----------------------------------------------------
    # CHECK WHETHER AGENT SELECTED A TOOL
    # -----------------------------------------------------

    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]


            # -------------------------------------------------
            # STUDY MATERIAL / RAG TOOL
            # -------------------------------------------------

            if tool_name == "study_material_tool":

                result = study_material_tool.invoke(
                    tool_args
                )

                return result


    # -----------------------------------------------------
    # NORMAL TEXT RESPONSE
    # -----------------------------------------------------

    if isinstance(response.content, str):

        return response.content


    # -----------------------------------------------------
    # GEMINI LIST RESPONSE
    # -----------------------------------------------------

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


        return "\n".join(text_parts)


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    return str(response.content)