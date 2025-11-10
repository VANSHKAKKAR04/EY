# backend/services/crm_api.py
import json
from pathlib import Path
from services.credit_api import get_credit_score  # Import to compute missing credit score

CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def get_customer_kyc(name: str):
    """Simulate CRM KYC lookup by matching partial name."""
    with open(CUSTOMERS_PATH, "r") as f:
        customers = json.load(f)

    for cust in customers:
        if name.lower() in cust["name"].lower():
            # Gracefully handle missing keys
            credit_score = cust.get("credit_score") or get_credit_score(name)
            preapproved_limit = cust.get("preapproved_limit", "Not available")
            city = cust.get("city", "Unknown")
            phone = cust.get("phone", "N/A")

            return {
                "name": cust["name"],
                "city": city,
                "phone": phone,
                "credit_score": credit_score,
                "preapproved_limit": preapproved_limit,
            }

    return None
