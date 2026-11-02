import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env file")

# Connect to Gemini
client = genai.Client(api_key=api_key)


def summarize_text(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Summarize the following study material.
        Use simple language and clear headings.
        Include the important concepts and key points.

        Study material:
        {text}
        """
    )

    return response.text