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
        }

    def handle_message(self, msg: str):
        msg_lower = msg.lower()
        stage = self.state["stage"]
        print(f"\n[DEBUG] MasterAgent handling stage='{stage}' | message='{msg}'")

        # === STAGE 1: Greeting ===
        if stage == "greeting":
            self.state["stage"] = "sales"
            return "👋 Hello! I’m your Tata Capital AI Assistant. Would you like to apply for a personal loan today?"

        # === STAGE 2: Sales Discussion ===
        elif stage == "sales":
            response, next_stage = self.sales.handle_sales(msg)

            # Capture context from SalesAgent
            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount")
            self.state["tenure"] = self.sales.context.get("tenure")

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === STAGE 3: KYC Verification ===
        elif stage == "kyc":
            print(f"[DEBUG] Handling KYC stage for message: '{msg}'")

            name = self.state.get("customer_name")
            requested_amount = self.state.get("loan_amount")

            if not name:
                print("[ERROR] Missing customer name during KYC.")
                return "Could you please confirm your full name again for KYC verification?"

            try:
                response = self.verify.perform_kyc(name, requested_amount)
            except Exception as e:
                print(f"[ERROR] KYC verification failed: {e}")
                return "I ran into an issue verifying your KYC. Please try again."

            if "verified" in response.lower():
                self.state["stage"] = "underwriting"
                return response + "\n✅ KYC verified! Now let’s check your loan eligibility."
            else:
                return response + "\nPlease re-enter your details."

        # === STAGE 4: Underwriting ===
        elif stage == "underwriting":
            print(f"[DEBUG] Handling underwriting stage for message='{msg}'")

            name = self.state.get("customer_name")
            amount = self.state.get("loan_amount")
            tenure = self.state.get("tenure", 3)

            if not name or not amount:
                print("[ERROR] Missing customer data during underwriting.")
                return "❌ Missing details — please re-enter your name and loan amount."

            # ✅ Pass amount explicitly to underwriting agent
            response, next_stage = self.underwrite.evaluate_loan(
                name, requested_amount=amount, interest_rate=12.0, tenure_years=tenure
            )

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === STAGE 5: Sanction Letter ===
        elif stage == "sanction":
            name = self.state["customer_name"]
            amount = self.state.get("loan_amount")
            tenure = self.state.get("tenure", 3)

            if not name:
                print("[ERROR] Missing name during sanction stage.")
                return "❌ Customer name missing — unable to generate sanction letter."

            # Ensure fallback amount if missing
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

            print(f"[DEBUG] Generating sanction letter for {name} | Amount: ₹{amount}")

            response = self.sanction.generate_letter(loan_data)
            self.state["stage"] = "complete"
            print(f"[DEBUG] Transitioning to next stage: complete")

            return (
                response
                + f"\n\n💰 Requested Loan Amount: ₹{amount:,.2f}"
                + "\n✅ Your sanction letter is now ready!"
            )

        # === STAGE 6: Completed ===
        elif stage == "complete":
            return "🎉 Your loan process is complete! Would you like to start a new application?"

        # === FALLBACK ===
        print("[DEBUG] Unrecognized stage or message. Returning fallback.")
        return "I didn’t quite get that — could you please rephrase?"
