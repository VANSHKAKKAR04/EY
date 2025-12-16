from utils.pdf_generator import generate_sanction_pdf, calculate_emi
from services.crm_api import get_customer_kyc
from services.credit_api import get_credit_score
from pathlib import Path
import requests


class SanctionAgent:
    def __init__(self):
        self.output_dir = Path("sanctions")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_letter(self, loan_data: dict):
        """
        Generates a sanction letter if all eligibility conditions are met.

        loan_data must include:
            {
                "name": str,
                "approved_amount": float,
                "interest_rate": float,
                "tenure": int,
                "purpose": str
            }

        Returns:
            (message: str, file_name: str | None)
        """

        # -------------------------------
        # 1️⃣ Mandatory validations
        # -------------------------------
        name = loan_data.get("name")
        if not name:
            return ("❌ Customer name missing — unable to generate sanction letter.", None)

        loan_purpose = loan_data.get("purpose")
        if not loan_purpose:
            return ("❌ Loan purpose missing — unable to generate sanction letter.", None)

        # -------------------------------
        # 2️⃣ Fetch CRM + Credit data
        # -------------------------------
        customer = get_customer_kyc(name)
        credit_score = get_credit_score(name)

        if not customer:
            return (f"❌ Customer '{name}' not found in CRM.", None)

        # Normalize CRM response
        if isinstance(customer, list):
            customer = customer[0]

        # -------------------------------
        # 3️⃣ Loan parameters
        # -------------------------------
        approved_amount = loan_data.get(
            "approved_amount",
            customer.get("preapproved_limit", 0)
        )
        rate = loan_data.get("interest_rate", 10.5)
        tenure = loan_data.get("tenure", 3)

        # -------------------------------
        # 4️⃣ EMI calculation
        # -------------------------------
        emi = calculate_emi(
            approved_amount,
            rate,
            tenure
        ) if tenure and tenure > 0 else 0.0

        # -------------------------------
        # 5️⃣ Generate sanction letter PDF
        # -------------------------------
        file_path = generate_sanction_pdf(
            name=name,
            loan_type=loan_purpose,
            amount=approved_amount,
            rate=rate,
            tenure=tenure,
            credit_score=credit_score
        )

        path_obj = Path(file_path)

        # -------------------------------
        # 6️⃣ Customer-facing message
        # -------------------------------
        message = (
            f"✅ Loan sanctioned for {name}!\n"
            f"Loan Type: {loan_purpose} Loan\n"
            f"Amount: ₹{approved_amount:,.2f} | "
            f"Interest: {rate:.2f}% | "
            f"Tenure: {tenure} years | "
            f"EMI: ₹{emi:,.2f}\n"
            f"Credit Score: {credit_score if credit_score is not None else 'Not available'}\n\n"
            f"📄 Your sanction letter is ready!"
        )

        # -------------------------------
        # 7️⃣ Save loan to Offer Mart
        # -------------------------------
        self.save_loan_to_offers(
            customer["id"],
            {
                "name": f"{loan_purpose} Loan",
                "type": loan_purpose.lower(),
                "amount": approved_amount,
                "interest_rate": rate,
                "tenure_months": tenure * 12,
                "status": "sanctioned",
                "sanction_letter_path": str(path_obj),
                "purpose": loan_purpose,
                "emi": emi,
            },
        )

        return message, path_obj.name

    # --------------------------------------------------
    def save_loan_to_offers(self, user_id: int, loan: dict):
        """Persist sanctioned loan via offer_mart_server."""
        try:
            response = requests.post(
                f"http://localhost:8002/user/{user_id}/loans",
                json=loan
            )
            if response.status_code == 200:
                print(f"[INFO] Loan saved for user {user_id}")
            else:
                print(
                    f"[WARN] Failed to save loan for user {user_id}: "
                    f"{response.status_code} | {response.text}"
                )
        except Exception as e:
            print(f"[ERROR] Error saving loan: {e}")
