from db import save_item
import os
import anthropic
from pypdf import PdfReader
from dotenv import load_dotenv
import json
from verify import parse_claude_output, verify_item

load_dotenv()

all_agenda_data = []
all_agenda_data_analyzed = []

client = anthropic.Anthropic()

pdf_folder = "../docs/test-data-cfisd"

pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")][:3]

for pdf_file in pdf_files:
    agenda_data = {"filename": pdf_file, "pages": []}
    raw_text = ""

    file_path = os.path.join(pdf_folder, pdf_file)
    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        raw_text += ", " + text
        if text:
            single_page = {"page_num": page_num, "page": text}
            agenda_data["pages"].append(single_page)

    all_agenda_data.append(agenda_data)

    raw_text = raw_text[:8000]

    prompt = f"""
    You are explaining local school board decisions to a parent or resident who has never attended a board meeting.

    Analyze the following agenda text and return a JSON array. Each object must have these exact keys:

    - "item_number": the label exactly as printed
    - "plain_summary": 1-2 sentences explaining what is being decided in plain English, as if texting a neighbor. No jargon. Say why a parent or resident should care.
    - "category": one of: tax_rate, zoning, school_policy, budget, contract, personnel, other
    - "amounts": list of any dollar amounts or rates mentioned, each as a string
    - "meeting_date": extract the meeting date from the text if visible, in YYYY-MM-DD format, or null if not found
    - "action_required": true if the board will vote on this item, false if it is just a discussion or presentation

    Raw Agenda Text:
    {raw_text}

    Return only the JSON array, no explanation, no markdown, no code blocks.
    """

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_response = response.content[0].text
    parsed_items = parse_claude_output(raw_response)

    verified_items = []
    for item in parsed_items:
        is_verified = verify_item(raw_text, item.get("plain_summary", ""))
        item["verified"] = is_verified
        verified_items.append(item)

    all_agenda_data_analyzed.append(verified_items)
    for item in verified_items:
        save_item(item, pdf_file, body="isd", body_name="Cypress-Fairbanks ISD")
    print(f"Saved {len(verified_items)} items from {pdf_file}")

print(f"Successfully processed {len(all_agenda_data)} CFISD agendas!")