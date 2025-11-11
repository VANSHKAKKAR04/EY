from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(title="Offer Mart Mock Server")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "offers.json"

# Load offers
with open(DATA_PATH, "r") as f:
    offers = json.load(f)

@app.get("/offers")
def get_all_offers():
    """Return all available loan offers."""
    return offers

@app.get("/offers/eligible")
def get_eligible_offers(salary: float):
    """Return offers that match a user's salary."""
    eligible = [o for o in offers if salary >= o["min_salary"]]
    if not eligible:
        return {"message": "No offers available for your salary range."}
    return eligible
