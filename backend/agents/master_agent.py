from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent


class MasterAgent:
    """
    Pipeline:

    greeting → sales → kyc → kyc_collect → (awaiting salary slip upload)
    → underwriting → sanction → complete
    """

    def __init__(self):
        self.sales = SalesAgent()
        self.verify = VerificationAgent()
        self.underwrite = UnderwritingAgent()
        self.sanction = SanctionAgent()

        self.state = {
            "stage": "greeting",
            # Sales input
            "customer_name": None,
            "loan_amount": None,
            "tenure": None,
            # Verified KYC
            "verified_customer": None,
        }

    # =================================================================
    def handle_message(self, msg: str):
        stage = self.state["stage"]
        print(f"\n[DEBUG] MasterAgent handling stage='{stage}' | message='{msg}'")

        # ============================================================
        # 1️⃣ GREETING
        # ============================================================
        if stage == "greeting":
            self.state["stage"] = "sales"
            return {
                "response": "👋 Hello! I’m your Tata Capital AI Assistant.\nWould you like to apply for a personal loan today?",
                "stage": "sales",
                "awaitingSalarySlip": False,
            }

        # ============================================================
        # 2️⃣ SALES STAGE
        # ============================================================
        elif stage == "sales":
            response, next_stage = self.sales.handle_sales(msg)

            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount")
            self.state["tenure"] = self.sales.context.get("tenure")

            if next_stage:
                self.state["stage"] = next_stage

            return {
                "response": response,
                "stage": next_stage or stage,
                "awaitingSalarySlip": False,
            }

        # ============================================================
        # 3️⃣ START KYC
        # ============================================================
        elif stage == "kyc":
            response = self.verify.start_kyc()
            self.state["stage"] = "kyc_collect"
            return {"response": response, "stage": "kyc_collect", "awaitingSalarySlip": False}

        # ============================================================
        # 3.1️⃣ KYC MULTI-STEP COLLECTION
        # ============================================================
        elif stage == "kyc_collect":
            response, kyc_complete, verified_record = self.verify.collect_step(msg)

            if "upload your salary slip" in response.lower():
                self.state["stage"] = "salary_slip"
                return {
                    "response": response,
                    "stage": "salary_slip",
                    "awaitingSalarySlip": True,
                }

            if kyc_complete:
                self.state["verified_customer"] = verified_record
                self.state["stage"] = "underwriting"
                return {
                    "response": response,
                    "stage": "underwriting",
                    "awaitingSalarySlip": False,
                }

            return {"response": response, "stage": "kyc_collect", "awaitingSalarySlip": False}

        # ============================================================
        # 4️⃣ UNDERWRITING
        # ============================================================
        elif stage == "underwriting":
            c = self.state["verified_customer"]
            amount = self.state["loan_amount"]
            tenure = self.state["tenure"]

            response, next_stage = self.underwrite.evaluate_loan(
                c["name"],
                requested_amount=amount,
                interest_rate=12.0,
                tenure_years=tenure,
            )

            if next_stage:
                self.state["stage"] = next_stage

            return {
                "response": response,
                "stage": next_stage or stage,
                "awaitingSalarySlip": False,
            }

        # ============================================================
        # 5️⃣ SANCTION LETTER
        # ============================================================
        elif stage == "sanction":
            c = self.state["verified_customer"]
            amount = self.state["loan_amount"]
            tenure = self.state["tenure"]

            loan_data = {
                "name": c["name"],
                "approved_amount": amount,
                "interest_rate": 10.5,
                "tenure": tenure,
                "age": c.get("age", 30),
            }

            letter = self.sanction.generate_letter(loan_data)
            self.state["stage"] = "complete"

            return {
                "response": letter
                + f"\n\n💰 Loan Amount: ₹{amount:,}"
                + "\n✅ Your sanction letter is ready!",
                "stage": "complete",
                "awaitingSalarySlip": False,
            }

        # ============================================================
        # 6️⃣ COMPLETED
        # ============================================================
        elif stage == "complete":
            return {
                "response": "🎉 Your loan journey is complete! Would you like to start a new application?",
                "stage": "complete",
                "awaitingSalarySlip": False,
            }

        # fallback
        return {"response": "I didn't quite get that — could you rephrase?", "stage": stage, "awaitingSalarySlip": False}

    # =================================================================
    # FILE UPLOAD HANDLER
    # =================================================================
    def handle_file_upload(self, filepath: str):
        print(f"[DEBUG] Received file upload: {filepath}")

        response, kyc_complete, record = self.verify.handle_salary_slip_upload(filepath)

        if kyc_complete:
            self.state["verified_customer"] = record
            self.state["stage"] = "underwriting"
            return {"response": response, "stage": "underwriting", "awaitingSalarySlip": False}

        return {"response": response, "stage": "salary_slip", "awaitingSalarySlip": True}
