import re
import json


def find_numbers(text):
    #Finds all numbers in a string, e.g. 475000, 8.5, 82
    return re.findall(r'\d+\.?\d*', text)


def verify_item(original_text, summary_text):
    """Checks that every number in the summary exists in the original text.
    Returns True if all numbers are verified, False if any were invented."""
    numbers_in_summary = find_numbers(summary_text)

    for number in numbers_in_summary:
        if number not in original_text:
            print(f"FAILED: {number} not found in original")
            return False

    return True


def parse_claude_output(raw_response):
    cleaned = raw_response.strip()
    # handle case where claude adds markdown wrapper anyway
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


if __name__ == "__main__":
    # test parse_claude_output
    test_response = '```json\n[{"item_number": "A", "text": "Contract for $475,000"}]\n```'
    print(parse_claude_output(test_response))

    # test verify_item
    original = "awarding a contract for 82 golf carts not to exceed $475,000"
    good_summary = "The city will buy 82 golf carts for up to $475,000"
    bad_summary = "The city will buy 82 golf carts for up to $999,000"

    print(verify_item(original, good_summary))
    print(verify_item(original, bad_summary))