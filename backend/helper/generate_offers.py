import json
import random
from pathlib import Path

# Output file path (adjust if needed)
OUTPUT_PATH = Path(__file__).resolve().parent / "offers.json"

# Loan categories
LOAN_TYPES = ["personal", "home", "auto"]

# Basic interest rate and amount ranges per category
OFFER_CONFIG = {
    "personal": {"interest": (10.0, 16.0), "max_amount": (100000, 2000000), "tenure": (12, 84), "min_salary": (20000, 80000)},
    "home": {"interest": (8.0, 10.5), "max_amount": (500000, 10000000), "tenure": (60, 360), "min_salary": (40000, 150000)},
    "auto": {"interest": (8.5, 12.5), "max_amount": (300000, 2000000), "tenure": (24, 96), "min_salary": (25000, 100000)},
}

DESCRIPTIONS = {
    "personal": "Flexible personal loan with quick approval and minimal documentation.",
    "home": "Affordable home loan with long-term repayment options and competitive rates.",
    "auto": "Easy car loan with fast disbursal and low EMIs."
}

def generate_offers(num_offers=500):
    offers = []
    for i in range(1, num_offers + 1):
        loan_type = random.choice(LOAN_TYPES)
        cfg = OFFER_CONFIG[loan_type]

        interest_rate = round(random.uniform(*cfg["interest"]), 2)
        max_amount = random.randrange(cfg["max_amount"][0], cfg["max_amount"][1], 50000)
        tenure_months = random.randrange(cfg["tenure"][0], cfg["tenure"][1], 12)
        min_salary = random.randrange(cfg["min_salary"][0], cfg["min_salary"][1], 5000)

        offer = {
            "id": i,
            "name": f"{loan_type.capitalize()} Loan Offer #{i}",
            "type": loan_type,
            "interest_rate": interest_rate,
            "max_amount": max_amount,
            "tenure_months": tenure_months,
            "min_salary": min_salary,
            "description": DESCRIPTIONS[loan_type]
        }

        offers.append(offer)

    return offers


if __name__ == "__main__":
    offers = generate_offers(500)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(offers, f, indent=2)

    print(f"✅ Generated {len(offers)} loan offers at: {OUTPUT_PATH}")
