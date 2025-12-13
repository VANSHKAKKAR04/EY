import json
from pathlib import Path
from services.credit_api import calculate_credit_score

CUSTOMERS_PATH = Path(__file__).resolve().parent / "data" / "customers.json"

customers = json.load(open(CUSTOMERS_PATH))

for c in customers:
    if "credit_score" not in c:
        c["credit_score"] = calculate_credit_score(c)

json.dump(customers, open(CUSTOMERS_PATH, "w"), indent=2)

print("Updated credit scores for all customers.")