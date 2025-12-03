from services.mistral_api import query_mistral
from services.rag_service import RAGService
import json
import re


class SalesAgent:
    """
    SalesAgent — ONLY handles the loan product discovery:
    - No personal identification here.
    - Collects loan amount, tenure, and loan purpose.
    - Passes control to KYC agent for customer identity verification.
    """

    def __init__(self, data_path="./data/customers.json"):
        print("[DEBUG] Initializing SalesAgent...")
        self.rag = RAGService(data_path)

        with open(data_path, "r") as f:
            self.customers = json.load(f)

        # Track loan details and purpose
        self.stage = "start"  # start → ask_amount → ask_tenure → ask_purpose → confirm
        self.context = {"amount": None, "tenure": None, "purpose": None}

        print("[DEBUG] SalesAgent loaded with", len(self.customers), "customers.")

    # -----------------------------------------------------
    def extract_loan_details(self, user_message: str):
        """Extract numeric loan amount and tenure in years."""
        print(f"[DEBUG] Extracting loan details from: '{user_message}'")

        cleaned = user_message.replace(",", "").lower()

        # Extract amount (numbers with 2-7 digits)
        amount_match = re.search(r'(\d{2,7})', cleaned)
        amount = int(amount_match.group(1)) if amount_match else None

        # Extract tenure (e.g. "5 years")
        tenure_match = re.search(r'(\d+)\s*(?:year|yr|yrs|years)', cleaned)
        tenure = int(tenure_match.group(1)) if tenure_match else None

        print(f"[DEBUG] Extracted amount={amount}, tenure={tenure}")
        return amount, tenure

    # -----------------------------------------------------
    def get_interest_rate(self, purpose: str, credit_score: int = 750) -> float:
        """Calculate interest rate based on loan purpose and credit score."""
        purpose_lower = purpose.lower()
        
        # Base rates by purpose
        base_rates = {
            "education": 8.5,
            "home": 7.5,
            "car": 9.0,
            "business": 10.5,
            "wedding": 11.0,
            "medical": 10.0,
            "consolidation": 11.5,
            "personal": 12.0,
        }
        
        # Find matching purpose
        base_rate = 12.0  # default
        for key, rate in base_rates.items():
            if key in purpose_lower:
                base_rate = rate
                break
        
        # Adjust based on credit score
        if credit_score >= 800:
            base_rate -= 1.5
        elif credit_score >= 750:
            base_rate -= 0.75
        elif credit_score < 700:
            base_rate += 2.0
        
        return round(base_rate, 2)

    # -----------------------------------------------------
    def handle_sales(self, user_message: str):
        """Main handler for the loan sales stage."""
        msg = user_message.strip()
        print(f"\n[DEBUG] SalesAgent stage='{self.stage}' | message='{msg}'")

        # Try extracting any amount/tenure the user might have mentioned
        amount, tenure = self.extract_loan_details(msg)

        # -------------------------------------------------
        # STEP 1 — Initial greeting inside Sales
        # -------------------------------------------------
        if self.stage == "start":
            self.stage = "ask_amount"
            print("[DEBUG] Transition to 'ask_amount'")
            return (
                "Great! Let's begin your loan application.\n"
                "Please tell me how much loan amount you are looking for.",
                None
            )

        # -------------------------------------------------
        # STEP 2 — Ask for loan amount
        # -------------------------------------------------
        elif self.stage == "ask_amount":
            if not amount:
                print("[DEBUG] No valid amount found.")
                return "Sure — please enter your desired loan amount in ₹.", None

            self.context["amount"] = amount
            self.stage = "ask_tenure"
            print(f"[DEBUG] Transition to 'ask_tenure' with amount={amount}")

            return (
                f"Got it! ₹{amount:,} noted.\n"
                "How many years would you like the repayment tenure to be?",
                None
            )

        # -------------------------------------------------
        # STEP 3 — Ask for tenure
        # -------------------------------------------------
        elif self.stage == "ask_tenure":
            if not tenure:
                print("[DEBUG] No valid tenure found.")
                return (
                    "Please mention the repayment period (e.g., 3 years, 5 years).",
                    None
                )

            self.context["tenure"] = tenure
            self.stage = "ask_purpose"

            print(f"[DEBUG] Transition to 'ask_purpose' | amount={self.context['amount']} | tenure={tenure}")
            return (
                f"Great! ₹{self.context['amount']:,} for {tenure} years noted.\n"
                "Now, may I ask — what is the primary purpose of this loan? "
                "(e.g., education, home, car, business, wedding, medical, debt consolidation, personal)",
                None
            )

        # -------------------------------------------------
        # STEP 4 — Ask for loan purpose
        # -------------------------------------------------
        elif self.stage == "ask_purpose":
            if not msg or len(msg.strip()) < 2:
                print("[DEBUG] No purpose provided.")
                return (
                    "Could you please tell me the purpose of your loan?",
                    None
                )

            self.context["purpose"] = msg.strip()
            self.stage = "confirm"

            print(f"[DEBUG] Transition to 'confirm' | purpose={self.context['purpose']}")

            prompt = f"""
            You are a professional Tata Capital AI Sales Assistant acting as a bank officer.
            The customer wants a loan of ₹{self.context['amount']} for {self.context['tenure']} years.
            Loan Purpose: {self.context['purpose']}

            Respond professionally:
            - Acknowledge and validate their loan purpose
            - Show empathy and understanding
            - Mention that interest rates are typically 8.5% to 13% depending on profile
            - Politely explain you'll now collect their KYC details and evaluate their profile
            - Ask them to proceed with the identity verification process
            
            Keep it warm and professional, like a bank officer would.
            """

            return query_mistral(prompt), "kyc"

        # -------------------------------------------------
        # STEP 5 — Final confirmation (fallback)
        # -------------------------------------------------
        elif self.stage == "confirm":
            print("[DEBUG] Final confirm stage")
            return (
                f"Perfect! Loan amount ₹{self.context['amount']:,} "
                f"for {self.context['tenure']} years (Purpose: {self.context['purpose']}) is confirmed.\n"
                "Let's proceed with KYC verification.",
                "kyc"
            )

        # -------------------------------------------------
        print("[DEBUG] Fallback reached")
        return "I didn't quite understand — could you rephrase?", None
