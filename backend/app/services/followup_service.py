import logging
from typing import Any

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_followup_question(
    survey_description: str,
    question_text: str,
    participant_answer: dict[str, Any] | None,
    question_description: str = "",
) -> str | None:
    """
    Determine if a follow-up question is needed based on the participant's answer.

    Args:
        survey_description: Description of the survey purpose
        question_text: Original question text
        participant_answer: Participant's answer to the original question
        question_description: Additional context about the question's purpose

    Returns:
        A follow-up question string or None if no follow-up is needed
    """
    if participant_answer is None:
        # No follow-up for skipped questions
        return None

    try:
        llm = ChatOpenAI(
            temperature=0.2,  # Keep temperature low for consistent outputs
            model_name=settings.CHAT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            max_tokens=100,  # Keep token limit small for short responses
        )

        # Format the system prompt to instruct the model
        system_prompt = """You are an expert survey analyst helping to improve data quality. 
        Your task is to decide if a short follow-up question would improve the quality of data collected.
        
        If the participant's answer is complete, specific, and provides enough context, respond with NONE.
        
        If the participant's answer is ambiguous, too general, or could benefit from a brief clarification,
        generate ONE short follow-up question that would improve the data quality.
        
        Keep follow-up questions brief, specific and directly related to the original question.
        Do not ask for personal information.
        """

        # Format the human message with survey context and the participant's answer
        human_prompt = f"""
        Survey topic: {survey_description}
        
        Original question: {question_text}
        """

        # Add question description if available
        if question_description:
            human_prompt += f"\n\nQuestion context: {question_description}"

        human_prompt += f"""
        
        Participant's answer: {participant_answer}
        
        Should I ask a follow-up? Respond with NONE if no follow-up is needed, or provide a short, specific follow-up question:
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt),
        ]

        # Get the response from the LLM
        response = await llm.ainvoke(messages)
        content = response.content.strip()

        # Return None if the model says no follow-up is needed
        if content.upper() == "NONE":
            return None

        return content

    except Exception as e:
        logger.error(f"Error generating follow-up question: {e}")
        # In case of error, don't generate a follow-up
        return None
