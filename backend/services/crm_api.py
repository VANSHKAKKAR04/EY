import json
from pathlib import Path
from services.credit_api import get_credit_score

# Path to CRM database
CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def _load_customers():
    """Internal function to load CRM data."""
    try:
        with open(CUSTOMERS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] customers.json not found at {CUSTOMERS_PATH}")
        return []


# ──────────────────────────────────────────────────────────
# 1. RETURN ALL CUSTOMERS (RAW)
# ──────────────────────────────────────────────────────────
def get_all_customers():
    """
    Returns full raw customer list for matching name, age, city, phone, salary.
    """
    return _load_customers()


# ──────────────────────────────────────────────────────────
# 2. GET CUSTOMER BY ID
# ──────────────────────────────────────────────────────────
def get_customer_by_id(cid: int):
    """Return a customer by ID."""
    customers = _load_customers()
    return next((c for c in customers if c["id"] == cid), None)


# ──────────────────────────────────────────────────────────
# 3. GET CUSTOMER BY NAME (EXACT MATCH OR PARTIAL)
# ──────────────────────────────────────────────────────────
def get_customer_kyc(name: str):
    """
    Fetch customers whose name matches (case-insensitive).
    Returns a LIST of matches (not a single dict).

    VerificationAgent handles:
      - multiple matches → ask for ID
      - single match → proceed
    """
    customers = _load_customers()

    matches = [
        cust for cust in customers
        if name.lower() in cust["name"].lower()
    ]

    # Add missing credit scores if needed
    for cust in matches:
        if not cust.get("credit_score"):
            cust["credit_score"] = get_credit_score(cust["name"])

    return matches
