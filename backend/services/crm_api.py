# backend/services/customer_service.py
import json
from pathlib import Path

CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def get_customer_kyc(name: str):
    with open(CUSTOMERS_PATH, "r") as f:
        data = json.load(f)
    return data.get(name)
