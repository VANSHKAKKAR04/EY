# master_agent.py

from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent
from services.crm_api import update_customer_loans


class MasterAgent:
    # ... (init and _create_response are correct and unchanged) ...
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
            "salary_slip_uploaded": False,
        }

    def _create_response(self, response_text, new_stage, slip=False, pan=False, aadhaar=False, file=None):
        """Helper to create consistent response structure, ensuring all flags are present."""
        return {
            "response": response_text,
            "stage": new_stage,
            "awaitingSalarySlip": slip,
            "awaitingPan": pan,
            "awaitingAadhaar": aadhaar,
            "file": file,
        }

    # =================================================================
    def handle_message(self, msg: str, user_profile: dict = None):
        self.user_profile = user_profile
        stage = self.state["stage"]
        print(f"\n[DEBUG] MasterAgent handling stage='{stage}' | message='{msg}'")

        # --------------------------------------------------------------
        # 1️⃣ GREETING (Unchanged)
        # --------------------------------------------------------------
        if stage == "greeting":
            msg_lower = msg.lower()
            if user_profile:
                name = user_profile.get("name") or "there"
                self.state["stage"] = "sales"
                self.sales.stage = "ask_amount"
                self.sales.context["name"] = name
                return self._create_response(
                    f"Hi {name}! I see you're logged in. Let's begin your loan application.\nPlease tell me how much loan amount you are looking for.",
                    "sales"
                )
            if any(word in msg_lower for word in ["yes", "yeah", "sure", "ok", "okay", "i need", "apply", "loan", "interested"]):
                self.state["stage"] = "sales"
                self.sales.stage = "ask_amount"
                return self._create_response(
                    "Great! Let's begin your loan application.\nPlease tell me how much loan amount you are looking for.",
                    "sales"
                )
            elif any(word in msg_lower for word in ["no", "nope", "not interested", "don't want"]):
                return self._create_response(
                    "I understand. Feel free to reach out anytime you're interested in applying for a loan. Have a great day! 👋",
                    "greeting"
                )
            else:
                return self._create_response(
                    "👋 Hello! I'm your Tata Capital AI Assistant.\nWould you like to apply for a personal loan today? (Yes/No)",
                    "greeting"
                )

        # --------------------------------------------------------------
        # 2️⃣ SALES STAGE (Unchanged)
        # --------------------------------------------------------------
        elif stage == "sales":
            if self.sales.stage == "start":
                self.sales.stage = "ask_amount"
            
            response, next_stage = self.sales.handle_sales(msg)
            self.state["customer_name"] = self.sales.context.get("name")
            self.state["loan_amount"] = self.sales.context.get("amount") or 0
            self.state["tenure"] = self.sales.context.get("tenure") or 0

            if next_stage:
                self.state["stage"] = next_stage

            return self._create_response(
                response,
                next_stage or stage,
            )

        # --------------------------------------------------------------
        # 3️⃣ KYC START (Unchanged)
        # --------------------------------------------------------------
        elif stage == "kyc":
            if self.user_profile:
                response = self.verify.start_kyc_for_profile(self.user_profile)
            else:
                response = self.verify.start_kyc()
            self.state["stage"] = "kyc_collect"
            return self._create_response(response, "kyc_collect")

        # --------------------------------------------------------------
        # 3.1️⃣ KYC MULTI-STEP COLLECTION (Text Input Stage)
        # --------------------------------------------------------------
        elif stage == "kyc_collect":
            response, kyc_complete, verified_record = self.verify.collect_step(msg)

            if isinstance(verified_record, list):
                verified_record = verified_record[0]

            # 1. TRANSITION TO PAN UPLOAD (After profile confirm/phone entry)
            if self.verify.step == "kyc_collect_pan_ready":
                self.state["stage"] = "pan_slip"
                return self._create_response(
                    response + "\n\n📄 Please upload your **PAN Card** document.", 
                    "pan_slip",
                    pan=True
                )
            
            # 2. KYC COMPLETE (Manual salary entry finished)
            if kyc_complete:
                self.state["verified_customer"] = verified_record
                self.state["stage"] = "underwriting"
                
                c = verified_record
                amount = self.state["loan_amount"] or 0
                tenure = self.state["tenure"] or 0

                response_eval, next_stage = self.underwrite.evaluate_loan(
                    c, requested_amount=amount, interest_rate=12.0, tenure_years=tenure,
                )

                if next_stage:
                    self.state["stage"] = next_stage

                return self._create_response(
                    response + "\n\n" + response_eval,
                    next_stage,
                    slip=next_stage == "salary_slip"
                )

            # 3. Normal text response (Stage remains kyc_collect)
            return self._create_response(response, "kyc_collect")

        # --------------------------------------------------------------
        # 3.2️⃣ NEW: PAN SLIP UPLOAD STAGE (Text input handler)
        # --------------------------------------------------------------
        elif stage == "pan_slip":
            # If user sends a message instead of uploading, re-prompt for the file
            return self._create_response(
                "⚠️ Please upload your PAN Card document to continue. Text input is not accepted in this stage.",
                "pan_slip",
                pan=True
            )

        # --------------------------------------------------------------
        # 3.3️⃣ NEW: AADHAAR SLIP UPLOAD STAGE (Text input handler)
        # --------------------------------------------------------------
        elif stage == "aadhaar_slip":
            # If user sends a message instead of uploading, re-prompt for the file
            return self._create_response(
                "⚠️ Please upload your Aadhaar Card document to continue. Text input is not accepted in this stage.",
                "aadhaar_slip",
                aadhaar=True
            )

        # --------------------------------------------------------------
        # 4️⃣ UNDERWRITING (Unchanged)
        # --------------------------------------------------------------
        elif stage == "underwriting":
            c = self.state["verified_customer"]
            if not c:
                return self._create_response("❌ No verified customer found.", "complete")

            if isinstance(c, list): c = c[0]; self.state["verified_customer"] = c
            amount = self.state["loan_amount"] or 0
            tenure = self.state["tenure"] or 0

            if self.state["salary_slip_uploaded"]:
                response = ("📄 Salary slip verified successfully.\n" "Proceeding with final approval...")
                self.state["stage"] = "sanction"
                return self._create_response(response, "sanction")

            response, next_stage = self.underwrite.evaluate_loan(
                c, requested_amount=amount, interest_rate=12.0, tenure_years=tenure,
            )

            if next_stage: self.state["stage"] = next_stage

            return self._create_response(response, next_stage, slip=next_stage == "salary_slip")

        # --------------------------------------------------------------
        # 5️⃣ SALARY SLIP UPLOAD STAGE (Unchanged)
        # --------------------------------------------------------------
        elif stage == "salary_slip":
            return self._create_response(
                "📄 Please upload your latest salary slip to continue.",
                "salary_slip",
                slip=True
            )

        # --------------------------------------------------------------
        # 6️⃣ SANCTION LETTER — Auto-generate (Unchanged)
        # --------------------------------------------------------------
        elif stage == "sanction":
            c = self.state["verified_customer"]
            if isinstance(c, list): c = c[0]
            amount = self.state["loan_amount"] or 0
            tenure = self.state["tenure"] or 0
            loan_purpose = self.sales.context.get("purpose") or "personal"
            credit_score = c.get("credit_score", 750)
            interest_rate = self.sales.get_interest_rate(loan_purpose, credit_score)
            loan_data = {
                "name": c["name"], "approved_amount": amount, "interest_rate": interest_rate,
                "tenure": tenure, "age": c.get("age", 30), "purpose": loan_purpose,
            }
            message, filename = self.sanction.generate_letter(loan_data)
            self.state["stage"] = "complete"
            update_customer_loans(c["id"])
            return self._create_response(
                message + f"\n\n💰 Loan Amount: ₹{amount:,} | Interest Rate: {interest_rate}%\n" + "✅ Your sanction letter is ready!",
                "complete",
                file=filename
            )

        # --------------------------------------------------------------
        # 7️⃣ COMPLETE (Unchanged)
        # --------------------------------------------------------------
        elif stage == "complete":
            return self._create_response(
                "🎉 Your loan journey is complete! Would you like to start a new application?",
                "complete"
            )

        return self._create_response("I didn't understand — could you rephrase?", stage)

    # =================================================================
    # FILE UPLOAD HANDLER (CRITICAL FIX FOR PAN/AADHAAR TRANSITION)
    # =================================================================
    def handle_file_upload(self, filepath: str):
        print(f"[DEBUG] Received file upload: {filepath} at stage {self.state['stage']} | Verify step: {self.verify.step}")

        current_stage = self.state["stage"]
        response, kyc_complete, updated_record = "", False, None
        
        # --- 1. PAN CARD UPLOAD STAGE ---
        if current_stage == "pan_slip":
            response, kyc_complete, updated_record = self.verify.handle_pan_upload(filepath)
            
            # Successful PAN upload transitions to Aadhaar upload stage
            if self.verify.step == "kyc_collect_aadhaar_ready":
                
                self.state["stage"] = "aadhaar_slip" # Set next stage
                
                return self._create_response(
                    response + "\n\n📄 Next, please upload your **Aadhaar Card** document.",
                    "aadhaar_slip", 
                    aadhaar=True
                )
            
            # If PAN upload fails, re-prompt on the pan_slip stage
            return self._create_response(
                response,
                "pan_slip",
                pan=True
            )
            
        # --- 2. AADHAAR CARD UPLOAD STAGE ---
        elif current_stage == "aadhaar_slip":
            response, kyc_complete, updated_record = self.verify.handle_aadhaar_upload(filepath)
            
            # Successful Aadhaar upload transitions back to kyc_collect for manual salary input
            if self.verify.step == "awaiting_salary":
                
                self.state["stage"] = "kyc_collect" # Set next stage
                
                return self._create_response(
                    response + "\n\nFinal step: Please enter your monthly salary (for cross-check).",
                    "kyc_collect"
                )
            
            # If Aadhaar upload fails, re-prompt on the aadhaar_slip stage
            return self._create_response(
                response,
                "aadhaar_slip",
                aadhaar=True
            )


        # --- 3. SALARY SLIP UPLOAD (Conditional by Underwriting) ---
        elif current_stage == "salary_slip":
            response, kyc_complete, updated_record = self.verify.handle_salary_slip_upload(filepath)
            
            if kyc_complete:
                self.state["verified_customer"] = updated_record
                self.state["salary_slip_uploaded"] = True
                self.state["stage"] = "underwriting"

                c = updated_record
                amount = self.state["loan_amount"] or 0
                tenure = self.state["tenure"] or 0

                response_eval, next_stage = self.underwrite.evaluate_loan(
                    c, requested_amount=amount, interest_rate=12.0, tenure_years=tenure,
                )

                if next_stage: self.state["stage"] = next_stage

                return self._create_response(
                    response + "\n\n" + response_eval,
                    next_stage,
                    slip=next_stage == "salary_slip"
                )
            
            # If salary slip fails, re-prompt on salary_slip stage
            return self._create_response(
                response,
                "salary_slip",
                slip=True
            )
            
        # --- FALLBACK ---
        return self._create_response(
            "⚠️ File upload received, but I was not expecting a document at this stage. Please continue the conversation.",
            current_stage,
            slip=current_stage == "salary_slip",
            pan=current_stage == "pan_slip",
            aadhaar=current_stage == "aadhaar_slip"
        )