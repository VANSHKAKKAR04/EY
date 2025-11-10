from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent


class MasterAgent:
    """
    MasterAgent — the orchestrator that manages the full loan journey:
    greeting → sales → kyc → underwriting → sanction → complete
    Each worker agent handles its own sub-task logic autonomously.
    """

    def __init__(self):
        # Initialize worker agents
        self.sales = SalesAgent()
        self.verify = VerificationAgent()
        self.underwrite = UnderwritingAgent()
        self.sanction = SanctionAgent()

        # Global master state
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

        # === STAGE 2: Sales Discussion (handled by SalesAgent) ===
        elif stage == "sales":
            response, next_stage = self.sales.handle_sales(msg)

            # Update master state with customer context
            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount")
            self.state["tenure"] = self.sales.context.get("tenure")

            # Transition control if SalesAgent completes its flow
            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === STAGE 3: KYC Verification (VerificationAgent) ===
        elif stage == "kyc":
            print(f"[DEBUG] Handling KYC stage for message: '{msg}'")

            # Allow user to ask sales-related or general questions mid-way
            if "limit" in msg_lower or "loan" in msg_lower:
                return (
                    "Your KYC verification is in progress. "
                    "Once verified, I can confirm your pre-approved limit."
                )

            name = self.state.get("customer_name")
            if not name:
                print("[ERROR] Missing customer name during KYC.")
                return "Could you please confirm your full name again for KYC verification?"

            try:
                response = self.verify.perform_kyc(name)
            except Exception as e:
                print(f"[ERROR] KYC verification failed: {e}")
                return "I ran into an issue verifying your KYC. Please try again."

            if "verified" in response.lower():
                self.state["stage"] = "underwriting"
                return response + "\n✅ KYC verified! Now let’s check your loan eligibility."
            else:
                return response + "\nPlease re-enter your details."


        # === STAGE 4: Underwriting (UnderwritingAgent) ===
        elif stage == "underwriting":
            name = self.state["customer_name"]
            amount = self.state["loan_amount"]
            tenure = self.state["tenure"]
            response, next_stage = self.underwrite.evaluate_loan(name, amount, tenure)

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === STAGE 5: Sanction Letter Generation (SanctionAgent) ===
        elif stage == "sanction":
            name = self.state["customer_name"]
            response, next_stage = self.sanction.generate_letter(name)

            if next_stage:
                self.state["stage"] = next_stage
                print(f"[DEBUG] Transitioning to next stage: {next_stage}")

            return response

        # === STAGE 6: Completed ===
        elif stage == "complete":
            return "🎉 Your loan process is complete! Would you like to start a new application?"

        # === FALLBACK ===
        print("[DEBUG] Unrecognized stage or message. Returning fallback.")
        return "I didn’t quite get that — could you please rephrase?"
