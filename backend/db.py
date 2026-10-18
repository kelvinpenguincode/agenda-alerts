import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
print("URL:", os.getenv("SUPABASE_URL"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

client = create_client(url, key)

def save_item(item, filename):
    data = {
        "id": filename + "-" + item["item_number"],
        "body": "city",
        "body_name": "City of Jersey Village",
        "meeting_date": filename,
        "item_number": item["item_number"],
        "text": item["text"],
        "verified": item["verified"],
        "filename": filename
    }

    result = client.table("agenda_items").upsert(data).execute()
    return result

if __name__ == "__main__":
    # test with a fake item
    test_item = {
        "item_number": "TEST-1",
        "text": "This is a test item",
        "verified": True
    }
    result = save_item(test_item, "test-file")
    print(result)