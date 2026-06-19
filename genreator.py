# src/generator.py

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def get_persona_prompt(persona):

    if persona == "Technical Expert":

        return """
        Act as Senior Support Engineer.

        Give:
        - Root cause analysis
        - Technical details
        - Logs
        - APIs
        - Step-by-step troubleshooting
        """

    elif persona == "Frustrated User":

        return """
        Act as empathetic support specialist.

        Begin with empathy.

        Use simple bullet points.

        Avoid jargon.
        """

    else:

        return """
        Act as business support manager.

        Focus on:

        - Impact
        - Resolution timeline
        - Business outcome

        Keep concise.
        """


def generate_response(
    query,
    persona,
    contexts
):

    context_text = "\n\n".join(
        [
            c["text"]
            for c in contexts
        ]
    )

    system_prompt = f"""
    {get_persona_prompt(persona)}

    Answer ONLY using context.

    Context:
    {context_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2
        )
    )

    return response.text