from fastapi import FastAPI
from pydantic import BaseModel
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1"

app = FastAPI()


# -----------------------
# Request model
# -----------------------
class TextInput(BaseModel):
    text: str


# -----------------------
# Extraction function
# -----------------------
def build_prompt(text: str):
    return f"""
Przetwórz poniższy tekst i zwróć wynik w formacie JSON o strukturze:
{{
    "pet_name": "",
    "breed": "",
    "sex": "",
    "age": "",
    "coat": "",
    "weight": "",
    "interview_description": "",
    "treatment_description": "",
    "applied_medicines": "",
    "recommendation": ""
}}

Tekst źródłowy:
----------------
{text}
"""


# -----------------------
# Main API endpoint
# -----------------------
@app.post("/extract")
async def extract_info(payload: TextInput):
    prompt = build_prompt(payload.text)

    response = openai.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Jesteś asystentem do ekstrakcji danych medycznych o zwierzętach.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    data = json.loads(response.choices[0].message.content)
    return data


# run server:
# uvicorn extract_server:app --reload
