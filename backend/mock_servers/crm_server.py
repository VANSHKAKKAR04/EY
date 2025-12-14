from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from pydantic import BaseModel
from services.crm_api import get_all_customers, sign_up, authenticate

app = FastAPI(title="CRM Mock Server")

# Allow cross-origin requests for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"


# Small schemas for signup/login
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


@app.get("/customers")
def get_all_customers_endpoint():
    return get_all_customers()


@app.get("/customers/{name}")
def get_customer_by_name(name: str):
    for c in get_all_customers():
        if c["name"].lower() == name.lower():
            return c
    return {"error": f"Customer '{name}' not found."}


@app.post("/signup")
def signup_endpoint(payload: SignUpIn):
    try:
        created = sign_up(
            name=payload.name,
            age=payload.age,
            city=payload.city,
            phone=payload.phone,
            salary=payload.salary,
            email=payload.email,
            password=payload.password,
            pan_number=payload.pan_number,
            aadhaar_number=payload.aadhaar_number,
        )
        return {"success": True, "customer": created}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
def login_endpoint(payload: LoginIn):
    user = authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "customer": user}
