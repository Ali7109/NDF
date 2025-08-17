import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")

supabase = create_client(SUPA_URL, SUPA_KEY)


def save_apod(date, title, explanation, url):
    response = (
        supabase.table("apod")
        .upsert({"date": date, "title": title, "explanation": explanation, "url": url})
        .execute()
    )

    return response


def get_all_apods():
    """Fetch all APOD records from the Supabase database."""
    response = supabase.table("apod").select("*").order("date", desc=True).execute()
    return response.data
