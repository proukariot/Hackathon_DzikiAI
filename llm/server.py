import json
import os
from io import BytesIO

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from pypdf import PdfReader
import openai

from supabase import create_client, Client
from sql_db.visit import Visit

# -----------------------
# Config
# -----------------------
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4.1")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


# ============================================================
# 🟦 LLM PART – TEXT & PDF EXTRACTION
# ============================================================

class TextInput(BaseModel):
    text: str


def build_prompt(text: str) -> str:
    # Build prompt for medical data extraction
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


def extract_from_text(text: str) -> dict:
    # Call OpenAI to extract structured data
    prompt = build_prompt(text)

    response = openai.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content": "Jesteś asystentem do ekstrakcji danych medycznych o zwierzętach."},
            {"role": "user", "content": prompt},
        ],
    )

    data = json.loads(response.choices[0].message.content)
    return data


def read_pdf_bytes(pdf_bytes: bytes) -> str:
    # Read PDF from bytes and return its extracted text
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


@app.post("/extract")
async def extract_info(payload: TextInput):
    """
    LLM: Extract structured data from plain text.
    """
    return extract_from_text(payload.text)


@app.post("/extract_pdf")
async def extract_info_from_pdf(file: UploadFile = File(...)):
    """
    LLM: Extract structured data from uploaded PDF file.
    """
    pdf_bytes = await file.read()
    pdf_text = read_pdf_bytes(pdf_bytes)
    return extract_from_text(pdf_text)


# ============================================================
# 🟩 SQL PART – SUPABASE DATABASE OPERATIONS
# ============================================================

@app.post("/add_visit")
def add_visit(visit: Visit):
    """
    SQL: Insert new visit into Supabase.
    """
    payload = visit.get_payload()
    result = supabase.table("visits").insert(payload).execute()
    return {"status": "ok", "data": result.data}


@app.get("/visits")
def get_all_visits():
    """
    SQL: Get all visits.
    """
    result = supabase.table("visits").select(
        "*").order("id_visit", desc=True).execute()
    return result.data


@app.get("/animals")
def get_all_animals():
    """
    SQL: Get all animals.
    """
    result = supabase.table("animals").select(
        "*").order("id_animal", desc=True).execute()
    return result.data


# ============================================================
# 🟧 HEALTH CHECK
# ============================================================

@app.get("/")
def health():
    return {"status": "ok"}
