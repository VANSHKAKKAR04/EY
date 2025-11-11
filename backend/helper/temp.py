import json
from pathlib import Path
import random

# Optional: import your credit score generator if available
try:
    from services.credit_api import get_credit_score
except ImportError:
    get_credit_score = lambda name: random.randint(650, 800)

# Path to your existing customers.json
CUSTOMERS_PATH = Path(__file__).resolve().parent/ "data" / "customers.json"

def normalize_customer_data():
    """Normalize all customer entries to a consistent schema."""
    try:
        with open(CUSTOMERS_PATH, "r") as f:
            customers = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not read customers.json: {e}")
        return

    updated_customers = []
    for i, cust in enumerate(customers, start=1):
        normalized = {
            "id": cust.get("id", i),
            "name": cust.get("name", f"Customer {i}"),
            "age": cust.get("age", random.randint(25, 60)),
            "city": cust.get("city", "Unknown"),
            "phone": cust.get("phone", f"9{random.randint(100000000, 999999999)}"),
            "salary": cust.get("salary", random.randint(30000, 150000)),
            "existing_loans": cust.get("existing_loans", random.randint(0, 3)),
            "credit_score": cust.get("credit_score") or get_credit_score(cust.get("name", "")),
            "preapproved_limit": cust.get("preapproved_limit", random.randint(100000, 800000)),
            "requested_loan": cust.get("requested_loan", cust.get("preapproved_limit", 0)),
        }
        updated_customers.append(normalized)

    # Backup the original file
    backup_path = CUSTOMERS_PATH.with_suffix(".backup.json")
    with open(backup_path, "w") as f:
        json.dump(customers, f, indent=2)
    print(f"[INFO] Backup created at {backup_path}")

    # Write normalized records
    with open(CUSTOMERS_PATH, "w") as f:
        json.dump(updated_customers, f, indent=2)
    print(f"[INFO] ✅ Normalized {len(updated_customers)} customer records successfully.")


if __name__ == "__main__":
    normalize_customer_data()
