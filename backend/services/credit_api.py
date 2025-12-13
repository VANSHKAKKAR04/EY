import random
import json
from pathlib import Path

CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"

def calculate_credit_score(customer: dict) -> int:
    """Calculate credit score based on customer's credit history and profile."""
    base = 750
    base -= customer.get("existing_loans", 0) * 25  # Penalty for existing loans
    base += min(customer.get("salary", 0) // 10000, 10) * 10  # Bonus for salary (up to 100k gives +100)
    base -= max(0, customer.get("age", 30) - 60)  # Penalty for age over 60
    return max(300, min(900, base))

_credit_cache = {}

def get_credit_score(name: str) -> int:
    if name not in _credit_cache:
        try:
            customers = json.load(open(CUSTOMERS_PATH))
            for c in customers:
                if c["name"] == name:
                    _credit_cache[name] = calculate_credit_score(c)
                    break
            else:
                _credit_cache[name] = 750  # Default if not found
        except:
            _credit_cache[name] = random.randint(650, 850)  # Fallback
    return _credit_cache[name]
