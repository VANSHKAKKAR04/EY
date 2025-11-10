from services.credit_api import get_credit_score
from services.crm_api import get_customer_kyc

class UnderwritingAgent:
    def evaluate_loan(
        self,
        name: str,
        requested_amount: float,
        interest_rate: float = 12.0,
        tenure_years: int = 3
    ):
        """
        Evaluate a customer's loan eligibility using mock credit and CRM data.
        Returns: (response_text, next_stage)
        """
        cust = get_customer_kyc(name)
        if not cust:
            return (f"❌ Customer '{name}' not found in CRM.", None)

        # --- Extract key data ---
        score = get_credit_score(name)
        pre_limit = cust.get("preapproved_limit", 0)
        salary = cust.get("salary", 0)

        # --- Stage 1: Credit score gate ---
        if score < 700:
            return (
                f"❌ Credit score {score} is below 700.\n"
                f"Loan cannot be approved at this time.",
                "complete",
            )

        # --- Stage 2: Instant approval (within pre-approved limit) ---
        if requested_amount <= pre_limit:
            return (
                f"✅ Instant Approval!\n"
                f"Credit Score: {score}\n"
                f"Requested: ₹{requested_amount:,.0f}\n"
                f"Within pre-approved limit of ₹{pre_limit:,.0f}.",
                "sanction",
            )

        # --- Stage 3: Conditional approval (up to 2× pre-limit) ---
        elif requested_amount <= 2 * pre_limit:
            emi = self.calculate_emi(requested_amount, interest_rate, tenure_years)
            max_emi = 0.5 * salary

            if emi <= max_emi:
                return (
                    f"✅ Conditional Approval\n"
                    f"Credit Score: {score}\n"
                    f"Requested: ₹{requested_amount:,.0f}\n"
                    f"EMI: ₹{emi:,.2f} (≤ 50% of salary ₹{salary:,.0f})\n"
                    f"Please upload your latest salary slip for verification.",
                    "sanction",
                )
            else:
                return (
                    f"⚠️ EMI ₹{emi:,.2f} exceeds 50% of salary ₹{salary:,.0f}.\n"
                    f"Loan cannot be approved without further review.",
                    "complete",
                )

        # --- Stage 4: Rejection ---
        return (
            f"❌ Requested ₹{requested_amount:,.0f} exceeds twice your "
            f"pre-approved limit (₹{2 * pre_limit:,.0f}).",
            "complete",
        )

    # -------------------------------------------
    @staticmethod
    def calculate_emi(principal: float, annual_rate: float, years: int) -> float:
        """Calculate EMI using reducing balance formula."""
        r = annual_rate / (12 * 100)
        n = years * 12
        if r == 0:
            return principal / n
        emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
        return emi
