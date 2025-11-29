from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from consts import *
from visit import Visit


app = FastAPI()


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.post("/add_visit")
def add_visit(visit: Visit):

    payload = visit.get_payload()
    result = supabase.table("wyzyta").insert(payload).execute()

    return {"status": "ok", "data": result.data}


@app.get("/all")
def get_all():
    result = supabase.table("messages").select("*").order("id", desc=True).execute()
    return result.data
