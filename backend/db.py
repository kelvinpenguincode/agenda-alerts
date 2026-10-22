import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

client = create_client(url, key)

def save_item(item, filename, body="city", body_name="City of Jersey Village"):
    data = {
        "id": filename + "-" + item["item_number"],
        "body": body,
        "body_name": body_name,
        "meeting_date": item.get("meeting_date") or filename,
        "item_number": item["item_number"],
        "plain_summary": item.get("plain_summary", ""),
        "category": item.get("category", "other"),
        "amounts": json.dumps(item.get("amounts", [])),
        "action_required": item.get("action_required", False),
        "verified": item["verified"],
        "filename": filename
    }
    result = client.table("agenda_items").upsert(data).execute()
    return result