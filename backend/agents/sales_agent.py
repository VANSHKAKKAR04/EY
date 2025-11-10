from services.mistral_api import query_mistral
from services.rag_service import RAGService
import json
import re


class SalesAgent:
    """
    SalesAgent — handles the conversational part of the loan sales journey.
    - Collects loan details step by step.
    - Retrieves customer profile (if found).
    - Keeps conversation focused on ONE customer.
    """

    def __init__(self, data_path="./data/customers.json"):
        print("[DEBUG] Initializing SalesAgent...")
        self.rag = RAGService(data_path)
        with open(data_path, "r") as f:
            self.customers = json.load(f)

        # Conversation state
        self.stage = "start"  # start → ask_name → ask_amount → ask_tenure → confirm
        self.context = {"name": None, "amount": None, "tenure": None}
        print("[DEBUG] SalesAgent initialized with", len(self.customers), "customers.")

    def extract_loan_details(self, user_message: str):
        """Extract numeric loan amount and tenure in years."""
        print(f"[DEBUG] Extracting loan details from message: '{user_message}'")
        amount_match = re.search(r'(\d{2,7})', user_message.replace(",", ""))
        tenure_match = re.search(r'(\d+)\s*(?:year|yr|yrs|years)', user_message.lower())

        amount = int(amount_match.group(1)) if amount_match else None
        tenure = int(tenure_match.group(1)) if tenure_match else None

        print(f"[DEBUG] Extracted amount={amount}, tenure={tenure}")
        return amount, tenure

    def get_customer_context(self, name_fragment: str):
        """Retrieve customer details by name or partial match."""
        print(f"[DEBUG] Searching for customer with name fragment: '{name_fragment}'")
        for cust in self.customers:
            if name_fragment.lower() in cust["name"].lower():
                print(f"[DEBUG] Found matching customer: {cust['name']}")
                return cust
        print("[DEBUG] No customer match found.")
        return None

    def handle_sales(self, user_message: str):
        """Handles user chat flow through the loan discussion phase."""
        msg = user_message.strip()
        print(f"\n[DEBUG] === Handling message: '{msg}' | Current stage: {self.stage} ===")

        amount, tenure = self.extract_loan_details(msg)

        # === Step 1: Greet user ===
        if self.stage == "start":
            self.stage = "ask_name"
            print("[DEBUG] Stage changed to 'ask_name'")
            return "👋 Great! Please share your full name so I can check your pre-approved offers.", None

        # === Step 2: Handle name ===
        elif self.stage == "ask_name":
            print("[DEBUG] Attempting RAG retrieval for name:", msg)
            context_docs = self.rag.retrieve(msg)
            print("[DEBUG] RAG retrieved", len(context_docs), "documents.")

            customer = self.get_customer_context(msg)

            if context_docs:
                context_text = context_docs[0]
                print("[DEBUG] Using RAG document for personalization.")
                prompt = f"""
                You are a Tata Capital AI assistant helping with loan sales.
                The customer has just entered their name: "{msg}".

                Retrieved background info:
                {context_text}

                Based on this, acknowledge the customer by name and mention:
                - Their pre-approved loan limit
                - Their credit score
                - Ask politely for the loan amount they wish to apply for
                """
                self.stage = "ask_amount"
                self.context["name"] = msg
                print(f"[DEBUG] Stage changed to 'ask_amount' for customer: {msg}")
                return query_mistral(prompt), None

            elif customer:
                print("[DEBUG] Found customer locally:", customer["name"])
                self.stage = "ask_amount"
                self.context["name"] = customer["name"]
                response = (
                    f"Thanks {customer['name']}! Based on our records, "
                    f"your pre-approved limit is ₹{customer['preapproved_limit']} "
                    f"and your credit score is {customer['credit_score']}.\n"
                    f"Please tell me the loan amount you wish to apply for."
                )
                return response, None

            else:
                print("[DEBUG] No RAG or local customer match found.")
                self.stage = "ask_amount"
                self.context["name"] = msg
                return f"Thanks {msg}! Please tell me the loan amount you’re looking for.", None

        # === Step 3: Loan amount ===
        elif self.stage == "ask_amount":
            print("[DEBUG] Processing loan amount:", amount)
            if not amount:
                print("[DEBUG] No valid amount found.")
                return "Could you please mention the loan amount in ₹?", None

            self.context["amount"] = amount
            self.stage = "ask_tenure"
            print(f"[DEBUG] Stage changed to 'ask_tenure' with amount={amount}")
            return f"Got it! ₹{amount} noted. Now, how many years do you want the repayment tenure to be?", None

        # === Step 4: Tenure ===
        elif self.stage == "ask_tenure":
            print("[DEBUG] Processing tenure:", tenure)
            if not tenure:
                print("[DEBUG] No valid tenure found.")
                return "Please specify the repayment tenure (e.g., 3 years, 5 years).", None

            self.context["tenure"] = tenure
            self.stage = "confirm"
            name = self.context["name"]
            amount = self.context["amount"]
            print(f"[DEBUG] Stage changed to 'confirm' | name={name}, amount={amount}, tenure={tenure}")

            prompt = f"""
            You are a Tata Capital Sales Assistant AI.
            The customer "{name}" has requested a loan of ₹{amount} for {tenure} years.
            Mention that interest rate typically ranges 10.5%–14%.
            Give a polite, confident confirmation and encourage moving to KYC verification next.
            """
            return query_mistral(prompt), "kyc"

        # === Step 5: Confirm ===
        elif self.stage == "confirm":
            print("[DEBUG] Final confirmation stage reached.")
            response = (
                f"Thanks {self.context['name']}! Your loan of ₹{self.context['amount']} "
                f"for {self.context['tenure']} years has been noted. "
                "Let’s proceed to verify your KYC details."
            )
            return response, "kyc"

        # === Fallback ===
        print("[DEBUG] Reached fallback response.")
        return "I didn’t quite get that — could you rephrase?", None
