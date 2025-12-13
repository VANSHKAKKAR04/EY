from fastapi import FastAPI
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Offer Mart Mock Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data"

# Load offers
with open(DATA_PATH / "offers.json", "r") as f:
    offers = json.load(f)

class Loan(BaseModel):
    name: str
    type: str
    amount: float
    interest_rate: float
    tenure_months: int
    status: str
    sanction_letter_path: str = None
    purpose: str = None
    emi: float = None

@app.get("/user/{user_id}/loans")
def get_user_loans(user_id: int):
    """Return all existing loan requests for a given user."""
    user_entry = next((o for o in offers if o["id"] == user_id), None)
    if not user_entry:
        return {"loans": []}
    return {"loans": user_entry["Loans"]}

@app.post("/user/{user_id}/loans")
def add_user_loan(user_id: int, loan: Loan):
    """Add a new loan for a given user."""
    user_entry = next((o for o in offers if o["id"] == user_id), None)
    if not user_entry:
        user_entry = {"id": user_id, "Loans": []}
        offers.append(user_entry)
    loan_dict = loan.dict()
    loan_dict["id"] = f"{user_id}_{len(user_entry['Loans']) + 1}"
    user_entry["Loans"].append(loan_dict)
    with open(DATA_PATH / "offers.json", "w") as f:
        json.dump(offers, f, indent=2)
    return {"message": "Loan added successfully"}
