from services.credit_api import get_credit_score
from services.crm_api import get_customer_kyc

class UnderwritingAgent:
    def evaluate_loan(self, name: str, interest_rate: float = 12.0, tenure_years: int = 3):
        """
        Evaluate a customer's loan eligibility using mock credit and CRM data.

        Rules:
        1️⃣ Reject if credit score < 700.
        2️⃣ Approve instantly if requested_loan ≤ preapproved_limit.
        3️⃣ If ≤ 2× preapproved_limit → request salary slip, approve only if EMI ≤ 50% of salary.
        4️⃣ Reject if > 2× preapproved_limit.
        """
        cust = get_customer_kyc(name)
        if not cust:
            return f"❌ Customer '{name}' not found in CRM."

        # Fetch data
        score = get_credit_score(name)
        requested = cust.get("requested_loan", 0)
        pre_limit = cust.get("preapproved_limit", 0)
        salary = cust.get("salary", 0)

        # 1️⃣ Credit score gate
        if score < 700:
            return f"❌ Credit score {score} is below 700. Loan cannot be approved."

        # 2️⃣ Instant approval
        if requested <= pre_limit:
            return (
                f"✅ Approved instantly!\n"
                f"Credit Score: {score}\n"
                f"Requested: ₹{requested}\n"
                f"Within pre-approved limit of ₹{pre_limit}."
            )

        # 3️⃣ Conditional approval (needs salary check)
        elif requested <= 2 * pre_limit:
            # Estimate EMI using reducing balance formula
            emi = self.calculate_emi(requested, interest_rate, tenure_years)
            max_emi = 0.5 * salary

            if emi <= max_emi:
                return (
                    f"✅ Conditional Approval\n"
                    f"Credit Score: {score}\n"
                    f"EMI: ₹{emi:.2f} (≤ 50% of salary ₹{salary})\n"
                    f"Please upload your latest salary slip for verification."
                )
            else:
                return (
                    f"⚠️ EMI ₹{emi:.2f} exceeds 50% of salary ₹{salary}.\n"
                    f"Loan cannot be approved without further review."
                )

        # 4️⃣ Rejection
        else:
            return (
                f"❌ Requested ₹{requested} exceeds 2× your limit (₹{2 * pre_limit})."
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
