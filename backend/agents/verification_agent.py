# verification_agent.py (Revised structure)

from services.crm_api import get_all_customers
from services.credit_api import get_credit_score
from services.ocr_utils import (
    validate_salary_slip,
    validate_pan_card,
    validate_aadhaar_card
)
from pathlib import Path


class VerificationAgent:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset temporary KYC session."""
        self.temp_data = {
            "name": None,
            "record": None,
            "pan_valid": False,
            "aadhaar_valid": False,
            "salary_slip_valid": False,
        }
        self.matches = []
        self.step = "awaiting_name"

    # ... (collect_step, start_kyc, start_kyc_for_profile are mostly untouched) ...

    def collect_step(self, msg: str):
        response = self.handle_kyc_input(msg)
        if self.step == "kyc_complete":
            return response, True, self.temp_data["record"]
        return response, False, None

    def start_kyc_for_profile(self, profile: dict):
        self.reset()
        self.temp_data["record"] = profile
        self.temp_data["name"] = profile.get("name")
        self.step = "awaiting_profile_confirm"
        parts = [
            f"Name: {profile.get('name', '')}", f"Age: {profile.get('age', '')}",
            f"City: {profile.get('city', '')}", f"Phone: {profile.get('phone', '')}",
            f"Salary: {profile.get('salary', '')}",
        ]
        summary = " | ".join(parts)
        return f"I have the following details for you: {summary}. Are these correct? (Yes/No)"

    # ------------------------------------------------------------------
    # MAIN INPUT HANDLER
    # ------------------------------------------------------------------
    def handle_kyc_input(self, msg: str):
        msg = msg.strip()

        # ---------------- PROFILE CONFIRMATION ------------------
        if self.step == "awaiting_profile_confirm":
            low = msg.lower()
            if any(w in low for w in ["yes", "y", "correct", "confirm"]):
                record = self.temp_data["record"]
                if "credit_score" not in record or record["credit_score"] is None:
                    record["credit_score"] = get_credit_score(record.get("name", ""))

                # Immediately transition to the dedicated PAN upload stage
                self.step = "kyc_collect_pan_ready" # Internal flag to tell MasterAgent to move stage
                return "Profile confirmed ✔️. Proceeding to document verification."
            else:
                self.reset()
                return "Okay — let's re-verify. Please enter your full legal name."

        # ... (Steps 1 to 4: awaiting_name, awaiting_id, awaiting_age, awaiting_city are UNCHANGED) ...

        # ---------------- STEP 5 — Phone ------------------
        if self.step == "awaiting_phone":
            actual = str(self.temp_data["record"]["phone"])

            if msg != actual:
                return "❌ Phone mismatch. Please re-enter the correct number."

            # Immediately transition to the dedicated PAN upload stage
            self.step = "kyc_collect_pan_ready" 
            return "Phone number verified ✔️. Proceeding to PAN card upload."

        # ---------------- STEP 6 — Awaiting Salary Input ------------------
        if self.step == "awaiting_salary":
            if not msg.isdigit():
                return "⚠️ Enter salary in numeric format."

            entered = int(msg)
            crm_salary = int(self.temp_data["record"]["salary"])

            if entered != crm_salary:
                return "❌ Salary mismatch. Enter the correct monthly salary."
            
            self.step = "kyc_complete"
            return "All key details verified ✔️.\n\nProceeding to loan evaluation."

        # --- New stages handled entirely by MasterAgent (handle_file_upload) ---
        # The agent should not receive messages in these states.
        if self.step == "kyc_collect_pan_ready":
             # This indicates the MasterAgent should transition to 'pan_slip'
             return "Ready for PAN upload." 
        if self.step == "kyc_collect_aadhaar_ready":
             # This indicates the MasterAgent should transition to 'aadhaar_slip'
             return "Ready for Aadhaar upload."
        if self.step == "awaiting_salary_slip":
             return "Waiting for salary slip..."

        if self.step == "kyc_complete":
            return "KYC already completed."

        return "❌ Unexpected error."

    # ------------------------------------------------------------------
    # DOCUMENT UPLOAD HANDLERS
    # ------------------------------------------------------------------

    def handle_pan_upload(self, file_path: str):
        """Process and validate the uploaded PAN document."""
        file_path = Path(file_path)
        record = self.temp_data["record"]
        customer_name = record.get("name", "")
        crm_pan = record.get("pan_number", "")

        result = validate_pan_card(customer_name, crm_pan, file_path) 
        
        status = result.get("status")
        msg = result.get("message", "")
        
        if status in ["error", "mismatch"]:
            return (f"❌ {msg}\n\nPlease try uploading a clear document again.", False, None)

        # SUCCESS
        self.temp_data["pan_valid"] = True
        
        # Next internal step is to transition to the dedicated Aadhaar upload stage
        self.step = "kyc_collect_aadhaar_ready" 
        return (
            f"PAN Card verified successfully ✔️.",
            False,
            record,
        )

    def handle_aadhaar_upload(self, file_path: str):
        """Process and validate the uploaded Aadhaar document."""
        file_path = Path(file_path)
        record = self.temp_data["record"]
        customer_name = record.get("name", "")
        crm_aadhaar = record.get("aadhaar_number", "")

        result = validate_aadhaar_card(customer_name, crm_aadhaar, file_path) 
        
        status = result.get("status")
        msg = result.get("message", "")

        if status in ["error", "mismatch"]:
            return (f"❌ {msg}\n\nPlease try uploading a clear document again.", False, None)

        # SUCCESS
        self.temp_data["aadhaar_valid"] = True
        
        # Next internal step is to return to the collection stage for manual salary input
        self.step = "awaiting_salary" 
        return (
            f"Aadhaar Card verified successfully ✔️.\n\nNow returning to final details entry.", 
            False, 
            record
        )
    
    # ... (handle_salary_slip_upload is UNCHANGED, but its next step is kyc_complete) ...
    def handle_salary_slip_upload(self, file_path: str):
        """
        Process and validate the uploaded salary slip.
        Returns (response, kyc_complete_flag, record)
        """
        file_path = Path(file_path)
        # Use OCR + CRM comparison
        result = validate_salary_slip(self.temp_data["name"], file_path)
        status = result.get("status")
        msg = result.get("message", "")

        if status == "error":
            return (f"❌ {msg}", False, None)
        if status == "mismatch":
            return (f"⚠️ {msg}", False, None)

        self.temp_data["salary_slip_valid"] = True
        record = self.temp_data["record"]
        if "credit_score" not in record or record["credit_score"] is None:
            record["credit_score"] = get_credit_score(record["name"])

        record["salary_slip_valid"] = True
        self.step = "kyc_complete"
        return (
            f"{msg}\n\n"
            "🎉 KYC Completed Successfully!\n\n"
            f"Name: {record['name']}\n"
            f"City: {record['city']}\n"
            f"Phone: {record['phone']}\n"
            f"Age: {record['age']}\n"
            f"Salary: ₹{record['salary']}\n"
            f"Credit Score: {record['credit_score']}\n"
            f"Pre-approved Limit: ₹{record.get('preapproved_limit',0):,}",
            True,
            record,
        )