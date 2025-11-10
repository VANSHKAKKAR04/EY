# backend/services/customer_service.py
import json
from pathlib import Path

CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def get_customer_kyc(name: str):
    """Simulate CRM KYC lookup by matching partial name."""
    with open(CUSTOMERS_PATH, "r") as f:
        customers = json.load(f)

    for cust in customers:
        if name.lower() in cust["name"].lower():
            return {
                "name": cust["name"],
                "city": cust["city"],
                "phone": cust["phone"],
                "credit_score": cust["credit_score"],
                "preapproved_limit": cust["preapproved_limit"],
            }
    return None
