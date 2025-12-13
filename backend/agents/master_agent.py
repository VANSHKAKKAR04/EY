from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent


class MasterAgent:
    """
    Correct Pipeline:
    greeting → sales → kyc → kyc_collect → underwriting
    → salary_slip (ONLY IF underwriting requests)
    → underwriting (final check) → sanction → complete
    """

    def __init__(self):
        self.sales = SalesAgent()
        self.verify = VerificationAgent()
        self.underwrite = UnderwritingAgent()
        self.sanction = SanctionAgent()

        self.user_profile = None

        self.state = {
            "stage": "greeting",
            "customer_name": None,
            "loan_amount": 0,
            "tenure": 0,
            "verified_customer": None,
            "salary_slip_uploaded": False,     # <--- NEW FLAG
        }

    # =================================================================
    def handle_message(self, msg: str, user_profile: dict = None):
        self.user_profile = user_profile
        stage = self.state["stage"]
        print(f"\n[DEBUG] MasterAgent handling stage='{stage}' | message='{msg}'")

        # --------------------------------------------------------------
        # 1️⃣ GREETING
        # --------------------------------------------------------------
        if stage == "greeting":
            # Check if user confirms they want to proceed
            msg_lower = msg.lower()
            # If a logged-in profile is provided, personalize and start sales
            if user_profile:
                name = user_profile.get("name") or "there"
                self.state["stage"] = "sales"
                self.sales.stage = "ask_amount"
                self.sales.context["name"] = name
                return {
                    "response": f"Hi {name}! I see you're logged in. Let's begin your loan application.\nPlease tell me how much loan amount you are looking for.",
                    "stage": "sales",
                    "awaitingSalarySlip": False,
                }
            if any(word in msg_lower for word in ["yes", "yeah", "sure", "ok", "okay", "i need", "apply", "loan", "interested"]):
                self.state["stage"] = "sales"
                # Initialize SalesAgent stage to ask_amount to skip the greeting
                self.sales.stage = "ask_amount"
                return {
                    "response": "Great! Let's begin your loan application.\nPlease tell me how much loan amount you are looking for.",
                    "stage": "sales",
                    "awaitingSalarySlip": False,
                }
            elif any(word in msg_lower for word in ["no", "nope", "not interested", "don't want"]):
                return {
                    "response": "I understand. Feel free to reach out anytime you're interested in applying for a loan. Have a great day! 👋",
                    "stage": "greeting",
                    "awaitingSalarySlip": False,
                }
            else:
                # Neutrally acknowledge and ask again
                return {
                    "response": "👋 Hello! I'm your Tata Capital AI Assistant.\nWould you like to apply for a personal loan today? (Yes/No)",
                    "stage": "greeting",
                    "awaitingSalarySlip": False,
                }

        # --------------------------------------------------------------
        # 2️⃣ SALES STAGE
        # --------------------------------------------------------------
        elif stage == "sales":
            # Ensure SalesAgent is in correct stage (skip initial "start" greeting)
            if self.sales.stage == "start":
                self.sales.stage = "ask_amount"
            
            response, next_stage = self.sales.handle_sales(msg)

            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount") or 0
            self.state["tenure"] = self.sales.context.get("tenure") or 0

            if next_stage:
                self.state["stage"] = next_stage

            return {
                "response": response,
                "stage": next_stage or stage,
                "awaitingSalarySlip": False,
            }

        # --------------------------------------------------------------
        # 3️⃣ KYC START
        # --------------------------------------------------------------
        elif stage == "kyc":
            if self.user_profile:
                response = self.verify.start_kyc_for_profile(self.user_profile)
            else:
                response = self.verify.start_kyc()
            self.state["stage"] = "kyc_collect"
            return {
                "response": response,
                "stage": "kyc_collect",
                "awaitingSalarySlip": False,
            }

        # --------------------------------------------------------------
        # 3.1️⃣ KYC MULTI-STEP COLLECTION
        # --------------------------------------------------------------
        elif stage == "kyc_collect":
            response, kyc_complete, verified_record = self.verify.collect_step(msg)

            if isinstance(verified_record, list):
                verified_record = verified_record[0]

            if kyc_complete:
                self.state["verified_customer"] = verified_record
                self.state["stage"] = "underwriting"
                
                # ✅ Auto-trigger underwriting immediately
                c = verified_record
                amount = self.state["loan_amount"] or 0
                tenure = self.state["tenure"] or 0

                # Evaluate loan automatically
                response_eval, next_stage = self.underwrite.evaluate_loan(
                    c,
                    requested_amount=amount,
                    interest_rate=12.0,
                    tenure_years=tenure,
                )

                if next_stage:
                    self.state["stage"] = next_stage

                awaiting_slip = next_stage == "salary_slip"

                return {
                    "response": response + "\n\n" + response_eval,
                    "stage": next_stage,
                    "awaitingSalarySlip": awaiting_slip,
                }

            return {
                "response": response,
                "stage": "kyc_collect",
                "awaitingSalarySlip": False,
            }

        # --------------------------------------------------------------
        # 4️⃣ UNDERWRITING
        # --------------------------------------------------------------
        elif stage == "underwriting":
            c = self.state["verified_customer"]
            if not c:
                return {
                    "response": "❌ No verified customer found.",
                    "stage": "complete",
                    "awaitingSalarySlip": False,
                }

            if isinstance(c, list):
                c = c[0]
                self.state["verified_customer"] = c

            amount = self.state["loan_amount"] or 0
            tenure = self.state["tenure"] or 0

            # If salary slip has already been uploaded → underwriting should NEVER ask again
            if self.state["salary_slip_uploaded"]:
                print("[DEBUG] Salary slip already uploaded → skip conditional check")

                response = (
                    "📄 Salary slip verified successfully.\n"
                    "Proceeding with final approval..."
                )

                # Immediate sanction
                self.state["stage"] = "sanction"
                return {
                    "response": response,
                    "stage": "sanction",
                    "awaitingSalarySlip": False,
                }

            # ---- NORMAL UNDERWRITING ----
            response, next_stage = self.underwrite.evaluate_loan(
                c,
                requested_amount=amount,
                interest_rate=12.0,
                tenure_years=tenure,
            )

            print("[DEBUG] Underwriting returned:", next_stage)

            if next_stage:
                self.state["stage"] = next_stage

            awaiting_slip = next_stage == "salary_slip"

            return {
                "response": response,
                "stage": next_stage,
                "awaitingSalarySlip": awaiting_slip,
            }

        # --------------------------------------------------------------
        # 5️⃣ SALARY SLIP UPLOAD STAGE
        # --------------------------------------------------------------
        elif stage == "salary_slip":
            return {
                "response": "📄 Please upload your latest salary slip to continue.",
                "stage": "salary_slip",
                "awaitingSalarySlip": True,
            }

        # --------------------------------------------------------------
        # 6️⃣ SANCTION LETTER — Auto-generate without user input
        # --------------------------------------------------------------
        elif stage == "sanction":
            c = self.state["verified_customer"]
            if isinstance(c, list):
                c = c[0]

            amount = self.state["loan_amount"] or 0
            tenure = self.state["tenure"] or 0
            
            # Calculate dynamic interest rate based on loan purpose and credit score
            loan_purpose = self.sales.context.get("purpose") or "personal"
            credit_score = c.get("credit_score", 750)
            interest_rate = self.sales.get_interest_rate(loan_purpose, credit_score)

            loan_data = {
                "name": c["name"],
                "approved_amount": amount,
                "interest_rate": interest_rate,
                "tenure": tenure,
                "age": c.get("age", 30),
                "purpose": loan_purpose,
            }

            message, filename = self.sanction.generate_letter(loan_data)
            self.state["stage"] = "complete"

            return {
                "response": message
                + f"\n\n💰 Loan Amount: ₹{amount:,} | Interest Rate: {interest_rate}%\n"
                + "✅ Your sanction letter is ready!",
                "stage": "complete",
                "awaitingSalarySlip": False,
                "file": filename,
            }

        # --------------------------------------------------------------
        # 7️⃣ COMPLETE
        # --------------------------------------------------------------
        elif stage == "complete":
            return {
                "response": "🎉 Your loan journey is complete! Would you like to start a new application?",
                "stage": "complete",
                "awaitingSalarySlip": False,
            }

        return {
            "response": "I didn't understand — could you rephrase?",
            "stage": stage,
            "awaitingSalarySlip": False,
        }

    # =================================================================
    # FILE UPLOAD HANDLER
    # =================================================================
    def handle_file_upload(self, filepath: str):
        print(f"[DEBUG] Received file upload: {filepath}")

        response, slip_accepted, updated_record = self.verify.handle_salary_slip_upload(filepath)

        if isinstance(updated_record, list):
            updated_record = updated_record[0]

        if slip_accepted:
            self.state["verified_customer"] = updated_record
            self.state["salary_slip_uploaded"] = True
            self.state["stage"] = "underwriting"

            # ✅ Auto-trigger underwriting immediately after salary slip validation
            c = updated_record
            amount = self.state["loan_amount"] or 0
            tenure = self.state["tenure"] or 0

            # Evaluate loan automatically with salary slip now available
            response_eval, next_stage = self.underwrite.evaluate_loan(
                c,
                requested_amount=amount,
                interest_rate=12.0,
                tenure_years=tenure,
            )

            if next_stage:
                self.state["stage"] = next_stage

            awaiting_slip = next_stage == "salary_slip"

            return {
                "response": response + "\n\n" + response_eval,
                "stage": next_stage,
                "awaitingSalarySlip": awaiting_slip,
            }

        return {
            "response": response,
            "stage": "salary_slip",
            "awaitingSalarySlip": True,
        }
