import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print([m.name for m in genai.list_models()])


# Load Gemini Pro model
model = genai.GenerativeModel("models/gemini-1.5-flash")


import re

def is_valid_query(query: str) -> bool:
    prompt = f"""
You're a smart assistant that checks whether a user's input can be answered using a web search.

If the input is a question like:
- "Best cafes in Connaught Place"
- "Weather in New York"
- "How to fix a flat tire"
Then reply with **"Yes"**.

If it's a command or unrelated like:
- "Add apples to grocery list"
- "Set an alarm"
Then reply with **"No"**.

Respond only with "Yes" or "No".

Input: "{query}"
"""
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip().lower()
        print("🟡 Gemini said:", repr(answer))  # <- log exactly what Gemini responded
        return re.match(r"^\s*yes\s*\.?\s*$", answer) is not None
    except Exception as e:
        print("[Gemini Error - is_valid_query]:", e)
        return False


def summarize_text(text: str) -> str:
    prompt = f"Summarize the following information for a general audience:\n\n{text[:8000]}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("[Gemini Error - summarize_text]:", e)
        return "Sorry, summarization failed."
