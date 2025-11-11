import requests

BASE_URL = "http://127.0.0.1:8002"

def get_all_offers():
    """Fetch all loan offers."""
    resp = requests.get(f"{BASE_URL}/offers")
    if resp.status_code == 200:
        return resp.json()
    return []

def get_eligible_offers(salary: float):
    """Fetch offers suitable for given salary."""
    resp = requests.get(f"{BASE_URL}/offers/eligible", params={"salary": salary})
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, list):
            return data
    return []
