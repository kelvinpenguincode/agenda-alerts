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
from db import client as supabase

load_dotenv()

app = FastAPI(title="Agenda Alerts API")

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
    query = supabase.table("agenda_items").select("*")
    if body:
        query = query.eq("body", body)
    result = query.execute()
    return result.data


@app.get("/api/lookup")
def lookup(address: str):
    geo = lookup_address(address)

    if not geo["covered"]:
        return {
            "covered": False,
            "reason": geo.get("reason", "We don't cover this area yet"),
            "items": []
        }

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
    home_value: float = Field(gt=0, description="Appraised home value in dollars")
    over_65: bool = Field(default=False, description="Is the homeowner over 65 or disabled?")


@app.post("/api/tax-impact")
def tax_impact(req: TaxImpactRequest):
    # CFISD homestead exemption: 20% of value + $140,000 flat
    exemption = (req.home_value * 0.20) + 140000

    # additional exemption for over 65 or disabled
    if req.over_65:
        exemption += 75000

    taxable_value = max(req.home_value - exemption, 0)

    # CFISD tax rates
    current_rate = 1.0869  # 2024
    proposed_rate = 1.0669  # 2025

    current_bill = taxable_value / 100 * current_rate
    proposed_bill = taxable_value / 100 * proposed_rate

    return {
        "home_value": req.home_value,
        "exemption": round(exemption, 2),
        "taxable_value": round(taxable_value, 2),
        "current_bill": round(current_bill, 2),
        "proposed_bill": round(proposed_bill, 2),
        "difference": round(proposed_bill - current_bill, 2),
        "note": "Estimate for CFISD school tax only. Does not include city, county, or other taxing units."
    }