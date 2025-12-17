from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.crm_api import get_all_customers, sign_up, authenticate

router = APIRouter(prefix="/crm", tags=["CRM"])

class SignUpIn(BaseModel):
    name: str
    age: int
    city: str
    phone: str
    salary: int
    email: str
    password: str
    pan_number: str
    aadhaar_number: str


class LoginIn(BaseModel):
    email: str
    password: str


@router.get("/customers")
def get_all_customers_endpoint():
    return get_all_customers()


@router.get("/customers/{name}")
def get_customer_by_name(name: str):
    for c in get_all_customers():
        if c["name"].lower() == name.lower():
            return c
    return {"error": f"Customer '{name}' not found."}


@router.post("/signup")
def signup_endpoint(payload: SignUpIn):
    try:
        created = sign_up(**payload.dict())
        return {"success": True, "customer": created}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_endpoint(payload: LoginIn):
    user = authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "customer": user}
