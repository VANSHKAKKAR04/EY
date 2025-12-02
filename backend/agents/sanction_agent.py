from utils.pdf_generator import generate_sanction_pdf, calculate_emi
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
        Returns a tuple: (message:str, file:str)
        """
        name = loan_data.get("name")
        if not name:
            return ("❌ Customer name missing — unable to generate sanction letter.", None)

        # Fetch supporting data
        customer = get_customer_kyc(name)
        credit_score = get_credit_score(name)

        if not customer:
            return (f"❌ Customer '{name}' not found in CRM.", None)

        # Normalize to dict if a list is returned
        if isinstance(customer, list):
            customer = customer[0]

        approved_amount = loan_data.get("approved_amount", customer.get("preapproved_limit", 0))
        rate = loan_data.get("interest_rate", 10.5)
        tenure = loan_data.get("tenure", 3)

        # Compute EMI and Generate PDF
        # Guard against invalid tenures
        emi = calculate_emi(approved_amount, rate, tenure) if tenure and tenure > 0 else 0.0
        file_path = generate_sanction_pdf(
            name=name,
            amount=approved_amount,
            rate=rate,
            tenure=tenure,
            credit_score=credit_score
        )

        path_obj = Path(file_path)  # ensure Path object

        message = (
            f"✅ Loan sanctioned for {name}!\n"
            f"Amount: ₹{approved_amount:,.2f} | Interest: {rate:.2f}% | Tenure: {tenure} years | EMI: ₹{emi:,.2f}\n"
            f"Credit Score: {credit_score if credit_score is not None else 'Not available'}\n\n"
            f"📄 Your sanction letter is ready!"
        )

        # Return both message and file name for frontend download
        return message, path_obj.name
