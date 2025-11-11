from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent


class MasterAgent:
    """
    MasterAgent — orchestrates the entire loan lifecycle:
    greeting → sales → kyc → underwriting → sanction → complete
    Each worker agent autonomously handles its sub-stage logic.
    """

    def __init__(self):
        self.sales = SalesAgent()
        self.verify = VerificationAgent()
        self.underwrite = UnderwritingAgent()
        self.sanction = SanctionAgent()

        self.state = {
            "stage": "greeting",
            "customer_name": None,
            "loan_amount": None,
            "tenure": None,
            "credit_score": None,
            "salary_slip_uploaded": False,
        }

    # ---------------------------------------------------
    def handle_message(self, msg: str):
        msg_lower = msg.lower()
        stage = self.state["stage"]
        print(f"\n[DEBUG] MasterAgent handling stage='{stage}' | message='{msg}'")

        # === 1️⃣ GREETING ===
        if stage == "greeting":
            self.state["stage"] = "sales"
            return (
                "👋 Hello! I’m your Tata Capital AI Assistant.\n"
                "Would you like to apply for a personal loan today?"
            )

        # === 2️⃣ SALES STAGE ===
        elif stage == "sales":
            response, next_stage = self.sales.handle_sales(msg)

            # Capture key context
            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount")
            self.state["tenure"] = self.sales.context.get("tenure")

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === 3️⃣ KYC VERIFICATION ===
        elif stage == "kyc":
            print(f"[DEBUG] Handling KYC stage for message: '{msg}'")

            name = self.state.get("customer_name")
            requested_amount = self.state.get("loan_amount")

            if not name:
                return "Could you please confirm your full name for KYC verification?"

            try:
                response = self.verify.perform_kyc(name, requested_amount)
            except Exception as e:
                print(f"[ERROR] KYC verification failed: {e}")
                return "❌ Error verifying KYC. Please try again."

            # If user needs to upload salary slip
            if "upload" in response.lower() or "salary slip" in msg_lower:
                self.state["stage"] = "await_upload"
                return (
                    response
                    + "\n📎 Please upload your latest salary slip to continue verification."
                )

            # If already verified (within pre-approved limit)
            if "verified" in response.lower():
                self.state["stage"] = "underwriting"
                return response + "\n✅ KYC verified! Moving to underwriting stage."

            return response

        # === 3.5️⃣ WAITING FOR UPLOAD ===
        elif stage == "await_upload":
            # Once frontend confirms upload done (via /upload-salary-slip)
            if "uploaded" in msg_lower or "done" in msg_lower:
                self.state["salary_slip_uploaded"] = True
                self.state["stage"] = "underwriting"
                return (
                    "📑 Salary slip received successfully.\n"
                    "✅ KYC verification completed.\n"
                    "Proceeding to underwriting stage..."
                )
            else:
                return (
                    "Please upload your salary slip using the upload button below "
                    "before we can continue."
                )

        # === 4️⃣ UNDERWRITING ===
        elif stage == "underwriting":
            print(f"[DEBUG] Handling underwriting stage for message='{msg}'")

            name = self.state.get("customer_name")
            amount = self.state.get("loan_amount")
            tenure = self.state.get("tenure", 3)

            if not name or not amount:
                return "❌ Missing details — please re-enter your name and loan amount."

            response, next_stage = self.underwrite.evaluate_loan(
                name, requested_amount=amount, interest_rate=12.0, tenure_years=tenure
            )

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === 5️⃣ SANCTION LETTER ===
        elif stage == "sanction":
            name = self.state["customer_name"]
            amount = self.state.get("loan_amount")
            tenure = self.state.get("tenure", 3)

            if not name:
                return "❌ Missing name — cannot generate sanction letter."

            if not amount or amount <= 0:
                from services.crm_api import get_customer_kyc
                cust = get_customer_kyc(name)
                amount = cust.get("preapproved_limit", 100000)

            loan_data = {
                "name": name,
                "approved_amount": amount,
                "interest_rate": 10.5,
                "tenure": tenure,
                "age": 30,
            }

            response = self.sanction.generate_letter(loan_data)
            self.state["stage"] = "complete"

            return (
                response
                + f"\n\n💰 Requested Loan Amount: ₹{amount:,.2f}"
                + "\n✅ Your sanction letter is now ready!"
            )

        # === 6️⃣ COMPLETE ===
        elif stage == "complete":
            return "🎉 Your loan process is complete! Would you like to start a new application?"

        # === FALLBACK ===
        print("[DEBUG] Unrecognized stage or message. Returning fallback.")
        return "I didn’t quite get that — could you please rephrase?"
