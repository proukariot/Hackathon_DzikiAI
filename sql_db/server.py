from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
#from consts import *
from visit import Visit
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI()
print(f"SUPABASE_URL: {SUPABASE_URL}, SUPABASE_KEY: {SUPABASE_KEY}")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.post("/add_visit")
def add_visit(visit: Visit):

    payload = visit.get_payload()
    result = supabase.table("visits").insert(payload).execute()

    return {"status": "ok", "data": result.data}


@app.get("/all_visits")
def get_all():
    result = supabase.table("visits").select("*").order("id_visit", desc=True).execute()
    return result.data


# start server:
# uvicorn server:app --reload --port 8000
