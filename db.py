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


def get_filtered_apods(filter):
    """Fetch APOD records where the title contains every word in filter_list."""
    filter_list = list(filter)
    query = supabase.table("apod").select("*")
    for word in filter_list:
        query = query.ilike("title", f"%{word}%")
    response = query.order("date", desc=True).execute()
    return response.data
