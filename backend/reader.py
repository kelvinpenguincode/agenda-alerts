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

pdf_folder = "../docs/test-data"

# grabs only the pdf files, limited to 3 for testing
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")][:3]

# loops through only the pdf files and extracts all the text into one large string
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

    # trim raw text so we don't send thousands of tokens to claude
    raw_text = raw_text[:8000]

    prompt = f"""
    You are an expert data parser for municipal government agendas. 
    Analyze the following raw agenda text and extract each item into a clean JSON array of objects.
    Each object must have these exact keys:
    - "item_number": The label or number of the item (e.g., "7.1", "A", "Item 3")
    - "text": The full description/content of the item
    
    Raw Agenda Text:
    {raw_text}
    """

    # sends raw text to claude and gets back structured JSON
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # parse claude's response and verify each item's numbers against the original text
    raw_response = response.content[0].text
    parsed_items = parse_claude_output(raw_response)



    verified_items = []
    for item in parsed_items:
        is_verified = verify_item(raw_text, item["text"])
        item["verified"] = is_verified
        verified_items.append(item)

    all_agenda_data_analyzed.append(verified_items)

# print results
for result in all_agenda_data_analyzed:
    print(result)
    print("---")

# save to file
with open("../docs/test-data/analyzed_agendas.json", "w") as f:
    json.dump(all_agenda_data_analyzed, f, indent=2)

print(f"Successfully processed {len(all_agenda_data)} agendas!")