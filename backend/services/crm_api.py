import json
from pathlib import Path
from services.credit_api import get_credit_score, calculate_credit_score

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


# ──────────────────────────────────────────────────────────
# 4. SIGNUP / AUTH HELPERS
# ──────────────────────────────────────────────────────────
def _save_customers(customers: list):
    """Write customers back to disk."""
    with open(CUSTOMERS_PATH, "w") as f:
        json.dump(customers, f, indent=2)


def _next_customer_id(customers: list) -> int:
    """Return next unique ID. New users start from 501 minimum."""
    if not customers:
        return 501
    max_id = max((c.get("id", 0) for c in customers), default=0)
    return max(max_id + 1, 501)


def _compute_preapproved_limit(salary: int) -> int:
    """Simple rule-based pre-approved limit based on salary."""
    if salary < 50000:
        return 200000
    if salary < 80000:
        return 400000
    if salary < 120000:
        return 600000
    return 800000


def sign_up(name: str, age: int, city: str, phone: str, salary: int, email: str, password: str) -> dict:
    """Register a new customer and persist to `customers.json`.

    - assigns a unique `id` (starts from 501)
    - computes `preapproved_limit` from `salary`
    - sets `existing_loans` to 0
    - stores a SHA256 hex digest of the password in `password_hash`
    - raises ValueError if email already exists
    """
    import hashlib

    customers = _load_customers()

    # email uniqueness check
    if any(c.get("email") and c["email"].lower() == email.lower() for c in customers):
        raise ValueError("Email already registered")

    cid = _next_customer_id(customers)

    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    new_customer = {
        "id": cid,
        "name": name,
        "age": age,
        "city": city,
        "phone": phone,
        "salary": salary,
        "preapproved_limit": _compute_preapproved_limit(salary),
        "existing_loans": 0,
        "email": email,
        "password_hash": pw_hash,
    }

    new_customer["credit_score"] = calculate_credit_score(new_customer)

    customers.append(new_customer)
    _save_customers(customers)

    # return a copy without the password hash
    safe = dict(new_customer)
    safe.pop("password_hash", None)
    return safe


def authenticate(email: str, password: str) -> dict:
    """Authenticate a user by email + password. Returns customer dict (no password_hash) or None."""
    import hashlib

    customers = _load_customers()
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    for c in customers:
        if c.get("email") and c["email"].lower() == email.lower():
            if c.get("password_hash") == pw_hash:
                safe = dict(c)
                safe.pop("password_hash", None)
                return safe
            return None

    return None


# ──────────────────────────────────────────────────────────
# 5. UPDATE CUSTOMER LOANS
# ──────────────────────────────────────────────────────────
def update_customer_loans(cid: int):
    """Increment existing_loans for a customer and update credit_score."""
    customers = _load_customers()
    for c in customers:
        if c["id"] == cid:
            c["existing_loans"] += 1
            c["credit_score"] = calculate_credit_score(c)
            _save_customers(customers)
            return True
    return False
