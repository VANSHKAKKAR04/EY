import json
from pathlib import Path
from services.credit_api import get_credit_score

# Define base URL (used if/when you expose CRM via API)
BASE_URL = "http://127.0.0.1:8001"

# Path to local dummy CRM database
CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def get_customer_kyc(name: str):
    """
    Simulate CRM KYC lookup.
    Matches partial name (case-insensitive) and returns enriched KYC info.
    """
    try:
        with open(CUSTOMERS_PATH, "r") as f:
            customers = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] customers.json not found at {CUSTOMERS_PATH}")
        return None

    for cust in customers:
        if name.lower() in cust["name"].lower():
            credit_score = cust.get("credit_score") or get_credit_score(name)

            return {
                "id": cust.get("id"),
                "name": cust["name"],
                "age": cust.get("age", "N/A"),
                "city": cust.get("city", "Unknown"),
                "phone": cust.get("phone", "N/A"),
                "salary": cust.get("salary", 0),
                # "credit_score": credit_score,
                "preapproved_limit": cust.get("preapproved_limit", 0),
                # "requested_loan": cust.get("requested_loan", cust.get("preapproved_limit", 0)),
                "existing_loans": cust.get("existing_loans", 0),
            }

    print(f"[INFO] No CRM record found for '{name}'.")
    return None
