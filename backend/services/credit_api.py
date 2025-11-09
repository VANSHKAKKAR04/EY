# backend/services/credit_api.py
import random

def get_credit_score(name: str) -> int:
    # mock deterministic score based on name hash
    random.seed(hash(name))
    return random.randint(600, 850)
