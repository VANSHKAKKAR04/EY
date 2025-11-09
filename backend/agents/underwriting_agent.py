# backend/agents/underwriting_agent.py
from services.credit_api import get_credit_score
from services.crm_api import get_customer_kyc

class UnderwritingAgent:
    def evaluate_loan(self, name: str):
        cust = get_customer_kyc(name)
        if not cust:
            return f"Customer '{name}' not found."

        score = get_credit_score(name)
        pre_limit = cust["pre_approved_limit"]
        requested = cust["requested_loan"]

        if score < 700:
            return f"❌ Credit score {score} is below 700. Loan cannot be approved."
        elif requested <= pre_limit:
            return f"✅ Approved instantly! Credit score {score}. Loan is within ₹{pre_limit} limit."
        elif requested <= 2 * pre_limit:
            return f"⚠️ Credit score {score}. Please upload salary slip for further evaluation."
        else:
            return f"❌ Requested ₹{requested} exceeds 2× limit ₹{2*pre_limit}."
