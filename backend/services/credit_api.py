import random

_credit_cache = {}

def get_credit_score(name: str) -> int:
    if name not in _credit_cache:
        _credit_cache[name] = random.randint(650, 850)
    return _credit_cache[name]
