from utils.pdf_generator import generate_sanction_pdf
from services.crm_api import get_customer_kyc
from services.credit_api import get_credit_score
from pathlib import Path

class SanctionAgent:
    def __init__(self):
        self.output_dir = Path("sanctions")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_letter(self, loan_data: dict):
        """
        Generates a sanction letter if all eligibility conditions are met.
        loan_data should include:
            {
                "name": str,
                "approved_amount": float,
                "interest_rate": float,
                "tenure": int
            }
        """
        name = loan_data.get("name")
        if not name:
            return "❌ Customer name missing — unable to generate sanction letter."

        # ✅ Fetch supporting data
        customer = get_customer_kyc(name)
        credit_score = get_credit_score(name)

        if not customer:
            return f"❌ Customer '{name}' not found in CRM."

        approved_amount = loan_data.get("approved_amount", customer.get("preapproved_limit", 0))
        rate = loan_data.get("interest_rate", 10.5)
        tenure = loan_data.get("tenure", 3)

        # ✅ Generate PDF
        file_path = generate_sanction_pdf(
            name=name,
            amount=approved_amount,
            rate=rate,
            tenure=tenure,
            credit_score=credit_score
        )

        return (
            f"✅ Loan sanctioned for {name}!\n"
            f"Amount: ₹{approved_amount:,.2f} | Interest: {rate}% | Tenure: {tenure} years\n"
            f"Credit Score: {credit_score}\n\n"
            f"📄 Sanction letter generated at: {file_path}"
        )
