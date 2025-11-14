from services.mistral_api import query_mistral
from services.rag_service import RAGService
import json
import re


class SalesAgent:
    """
    SalesAgent — ONLY handles the loan product discovery:
    - No personal identification here.
    - Collects loan amount and tenure.
    - Passes control to KYC agent for customer identity verification.
    """

    def __init__(self, data_path="./data/customers.json"):
        print("[DEBUG] Initializing SalesAgent...")
        self.rag = RAGService(data_path)

        with open(data_path, "r") as f:
            self.customers = json.load(f)

        # Only track loan details here
        self.stage = "start"  # start → ask_amount → ask_tenure → confirm
        self.context = {"amount": None, "tenure": None}

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
            self.stage = "confirm"

            print(f"[DEBUG] Transition to 'confirm' | amount={self.context['amount']} | tenure={tenure}")

            prompt = f"""
            You are a Tata Capital AI Sales Assistant.
            The customer wants a loan of ₹{self.context['amount']} for {tenure} years.

            Respond:
            - Acknowledge the amount and tenure
            - Mention typical interest range (10.5%–14%)
            - Politely ask to proceed to KYC next
            """

            return query_mistral(prompt), "kyc"

        # -------------------------------------------------
        # STEP 4 — Final confirmation (fallback)
        # -------------------------------------------------
        elif self.stage == "confirm":
            print("[DEBUG] Final confirm stage")
            return (
                f"Great! Loan amount ₹{self.context['amount']:,} "
                f"for {self.context['tenure']} years is noted.\n"
                "Let’s proceed with KYC verification.",
                "kyc"
            )

        # -------------------------------------------------
        print("[DEBUG] Fallback reached")
        return "I didn't quite understand — could you rephrase?", None
