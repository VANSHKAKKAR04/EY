from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(title="CRM Mock Server")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

# Load customers once at startup
with open(DATA_PATH, "r") as f:
    customers = json.load(f)

@app.get("/customers")
def get_all_customers():
    """Return all customers."""
    return customers

@app.get("/customers/{name}")
def get_customer_by_name(name: str):
    """Return KYC data for a given customer name."""
    for c in customers:
        if c["name"].lower() == name.lower():
            return c
    return {"error": f"Customer '{name}' not found."}
