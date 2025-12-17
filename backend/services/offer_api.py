import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OFFERS_FILE = DATA_DIR / "offers.json"


OFFERS_FILE = DATA_DIR / "offers.json"
print("Offers file exists:", OFFERS_FILE.exists())
print("Offers file path:", OFFERS_FILE)


def load_offers():
    if not OFFERS_FILE.exists():
        return []
    with open(OFFERS_FILE, "r") as f:
        return json.load(f)


def save_offers(offers):
    with open(OFFERS_FILE, "w") as f:
        json.dump(offers, f, indent=2)


def get_user_loans(user_id: int):
    offers = load_offers()
    print("Requested user_id:", user_id)
    print("Available offer IDs:", [o["id"] for o in offers])
    user = next((o for o in offers if o["id"] == user_id), None)

    if not user:
        return []

    # 🔥 MIGRATION FIX: normalize Loans → loans
    if "Loans" in user and "loans" not in user:
        user["loans"] = user.pop("Loans")
        save_offers(offers)

    return user.get("loans", [])


def add_user_loan(user_id: int, loan: dict):
    offers = load_offers()
    user = next((o for o in offers if o["id"] == user_id), None)

    if not user:
        user = {"id": user_id, "loans": []}
        offers.append(user)

    # 🔥 Ensure lowercase only
    if "Loans" in user:
        user["loans"] = user.pop("Loans")

    loan["id"] = f"{user_id}_{len(user['loans']) + 1}"
    user["loans"].append(loan)

    save_offers(offers)
    return loan
