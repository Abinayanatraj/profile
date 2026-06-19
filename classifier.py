# src/classifier.py

import json
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def classify_persona(user_message: str):

    schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": [
                    "Technical Expert",
                    "Frustrated User",
                    "Business Executive"
                ]
            },
            "confidence": {
                "type": "NUMBER"
            },
            "reasoning": {
                "type": "STRING"
            }
        },
        "required": [
            "persona",
            "confidence",
            "reasoning"
        ]
    }

    prompt = """
    Classify support user into ONE category:

    Technical Expert
    Frustrated User
    Business Executive

    Return valid JSON only.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.1
        )
    )

    return json.loads(response.text)