from fastapi import APIRouter
from pydantic import BaseModel
from services.offer_api import get_user_loans, add_user_loan

router = APIRouter(prefix="/offer-mart", tags=["Offer Mart"])

class Loan(BaseModel):
    name: str
    type: str
    amount: float
    interest_rate: float
    tenure_months: int
    status: str
    sanction_letter_path: str | None = None
    purpose: str | None = None
    emi: float | None = None


@router.get("/user/{user_id}/loans")
def get_loans(user_id: int):
    return {"loans": get_user_loans(user_id)}


@router.post("/user/{user_id}/loans")
def add_loan(user_id: int, loan: Loan):
    return {
        "message": "Loan added",
        "loan": add_user_loan(user_id, loan.dict())
    }
