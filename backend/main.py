"""Agenda Alerts backend.

Run from inside the backend/ folder:
    uvicorn main:app --reload --port 8000

Then open http://localhost:8000/docs to try every endpoint in the browser.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from db import save_item
from geo import lookup_address

# import supabase client from db.py
from db import client as supabase

load_dotenv()

app = FastAPI(title="Agenda Alerts API")

# which websites may call this API
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


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items(body: str | None = None):
    # reads from supabase instead of sample file
    query = supabase.table("agenda_items").select("*")
    if body:
        query = query.eq("body", body)
    result = query.execute()
    return result.data


@app.get("/api/lookup")
def lookup(address: str):
    # step 1: geocode the address
    geo = lookup_address(address)

    if not geo["covered"]:
        return {
            "covered": False,
            "reason": geo.get("reason", "We don't cover this area yet"),
            "items": []
        }

    # step 2: fetch matching items from supabase
    items = []

    if geo["city_covered"]:
        city_result = supabase.table("agenda_items").select("*").eq("body", "city").execute()
        items += city_result.data

    if geo["isd_covered"]:
        isd_result = supabase.table("agenda_items").select("*").eq("body", "isd").execute()
        items += isd_result.data

    return {
        "covered": True,
        "lat": geo["lat"],
        "lon": geo["lon"],
        "city": geo.get("city"),
        "isd": geo.get("isd"),
        "items": items
    }


class TaxImpactRequest(BaseModel):
    home_value: float = Field(gt=0, description="Appraised value of the home in dollars")
    exemption: float = Field(default=0, ge=0, description="Total exemptions in dollars")
    current_rate: float = Field(gt=0, description="Current rate per $100 of taxable value")
    proposed_rate: float = Field(gt=0, description="Proposed rate per $100 of taxable value")


@app.post("/api/tax-impact")
def tax_impact(req: TaxImpactRequest):
    taxable_value = max(req.home_value - req.exemption, 0)
    current_bill = taxable_value / 100 * req.current_rate
    proposed_bill = taxable_value / 100 * req.proposed_rate
    return {
        "taxable_value": round(taxable_value, 2),
        "current_bill": round(current_bill, 2),
        "proposed_bill": round(proposed_bill, 2),
        "difference": round(proposed_bill - current_bill, 2),
    }