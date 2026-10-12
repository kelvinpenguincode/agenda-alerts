"""Agenda Alerts backend (starter).

Run from inside the backend/ folder:
    uvicorn main:app --reload --port 8000

Then open http://localhost:8000/docs to try every endpoint in the browser.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"

app = FastAPI(title="Agenda Alerts API")

# Which websites may call this API. Locally the React dev server is on :5173.
# After deploying, add your Vercel URL to ALLOWED_ORIGINS (comma separated).
origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_items() -> list[dict]:
    """Right now this reads fake sample data. Later: read from the database."""
    with open(DATA_DIR / "sample_items.json", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items(body: str | None = None):
    """All agenda items. Optional filter: ?body=isd or ?body=city"""
    items = load_items()
    if body:
        items = [item for item in items if item["body"] == body]
    return items


class TaxImpactRequest(BaseModel):
    home_value: float = Field(gt=0, description="Appraised value of the home, in dollars")
    exemption: float = Field(default=0, ge=0, description="Total exemptions, in dollars")
    current_rate: float = Field(gt=0, description="Current rate per $100 of taxable value")
    proposed_rate: float = Field(gt=0, description="Proposed rate per $100 of taxable value")


@app.post("/api/tax-impact")
def tax_impact(req: TaxImpactRequest):
    """What a proposed tax rate does to one household's yearly bill.

    TODO (calculator owner): check this formula against your ISD's real
    tax-rate notice before trusting it - appraisal caps and exemptions
    differ by situation.
    """
    taxable_value = max(req.home_value - req.exemption, 0)
    current_bill = taxable_value / 100 * req.current_rate
    proposed_bill = taxable_value / 100 * req.proposed_rate
    return {
        "taxable_value": round(taxable_value, 2),
        "current_bill": round(current_bill, 2),
        "proposed_bill": round(proposed_bill, 2),
        "difference": round(proposed_bill - current_bill, 2),
    }
