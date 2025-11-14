from services.crm_api import get_all_customers
from services.credit_api import get_credit_score
from services.ocr_utils import validate_salary_slip
from pathlib import Path


class VerificationAgent:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset temporary KYC session."""
        self.temp_data = {
            "name": None,
            "record": None,
            "salary_slip_valid": False,
        }
        self.matches = []
        self.step = "awaiting_name"

    # ------------------------------------------------------------------
    # Compatibility wrapper for MasterAgent
    # ------------------------------------------------------------------
    def collect_step(self, msg: str):
        """
        returns -> response (str), kyc_complete (bool), record (dict|None)
        """
        response = self.handle_kyc_input(msg)

        if self.step == "kyc_complete":
            return response, True, self.temp_data["record"]

        return response, False, None

    # ------------------------------------------------------------------
    def start_kyc(self):
        self.reset()
        return "To begin the KYC process, please enter your full legal name."

    # ------------------------------------------------------------------
    # MAIN INPUT HANDLER
    # ------------------------------------------------------------------
    def handle_kyc_input(self, msg: str):
        msg = msg.strip()

        # ---------------- STEP 1 — Name ------------------
        if self.step == "awaiting_name":
            name = msg
            all_customers = get_all_customers()
            matches = [c for c in all_customers if c["name"].lower() == name.lower()]

            if not matches:
                return "❌ No customer found with that name. Please try again."

            self.temp_data["name"] = name

            if len(matches) > 1:
                self.matches = matches
                self.step = "awaiting_id"
                ids = ", ".join(str(c["id"]) for c in matches)
                return f"Multiple matches found. Please enter your Customer ID: {ids}"

            self.temp_data["record"] = matches[0]
            self.step = "awaiting_age"
            return "Please enter your age."

        # ---------------- STEP 2 — Customer ID ------------------
        if self.step == "awaiting_id":
            if not msg.isdigit():
                return "⚠️ Please enter a numeric ID."

            cid = int(msg)
            chosen = next((c for c in self.matches if c["id"] == cid), None)
            if not chosen:
                return "❌ Invalid ID. Choose from the list."

            self.temp_data["record"] = chosen
            self.step = "awaiting_age"
            return "Please enter your age."

        # ---------------- STEP 3 — Age ------------------
        if self.step == "awaiting_age":
            if not msg.isdigit():
                return "⚠️ Age must be a number."

            if int(msg) != self.temp_data["record"]["age"]:
                return "❌ Age mismatch. Please re-enter correctly."

            self.step = "awaiting_city"
            return "Please enter your city."

        # ---------------- STEP 4 — City ------------------
        if self.step == "awaiting_city":
            if msg.lower() != self.temp_data["record"]["city"].lower():
                return "❌ City mismatch. Please try again."

            self.step = "awaiting_phone"
            return "Please enter your registered phone number."

        # ---------------- STEP 5 — Phone ------------------
        if self.step == "awaiting_phone":
            actual = str(self.temp_data["record"]["phone"])

            if msg != actual:
                return "❌ Phone mismatch. Please re-enter the correct number."

            self.step = "awaiting_salary"
            return "Please enter your monthly salary."

        # ---------------- STEP 6 — Salary ------------------
        if self.step == "awaiting_salary":
            if not msg.isdigit():
                return "⚠️ Enter salary in numeric format."

            entered = int(msg)
            crm_salary = int(self.temp_data["record"]["salary"])

            if entered != crm_salary:
                return "❌ Salary mismatch. Enter the correct monthly salary."

            # All details matched — now request salary slip
            self.step = "awaiting_salary_slip"
            return (
                "All details verified ✔️\n"
                "📄 Please upload your salary slip for validation."
            )

        # ---------------- STEP 7 — Waiting for Salary Slip ------------------
        if self.step == "awaiting_salary_slip":
            return (
                "📄 Waiting for salary slip…\n"
                "Please upload your salary slip using the upload button."
            )

        # ---------------- STEP 8 — After completion ------------------
        if self.step == "kyc_complete":
            return "KYC already completed."

        return "❌ Unexpected error."

    # ------------------------------------------------------------------
    # SALARY SLIP UPLOAD HANDLER (called from MasterAgent)
    # ------------------------------------------------------------------
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

        # SUCCESS
        self.temp_data["salary_slip_valid"] = True

        record = self.temp_data["record"]

        # Add credit score if missing
        if "credit_score" not in record or record["credit_score"] is None:
            record["credit_score"] = get_credit_score(record["name"])

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
