from services.credit_api import get_credit_score
from services.crm_api import get_customer_kyc
from utils.pdf_generator import calculate_emi


class UnderwritingAgent:

    def evaluate_loan(
        self,
        customer,              
        requested_amount: float,
        interest_rate: float = 12.0,
        tenure_years: int = 3
    ):
        """
        Correct underwriting logic:
        - Salary slip is ONLY needed when:
            pre_limit < requested_amount <= 2 * pre_limit
        """
        if not isinstance(customer, dict):
            return "❌ Invalid customer data received.", "complete"

        name = customer.get("name")
        if not name:
            return "❌ Customer name missing.", "complete"

        salary = customer.get("salary", 0)
        pre_limit = customer.get("preapproved_limit", 0)

        # 1. Get credit score
        score = customer.get("credit_score") or get_credit_score(name)

        # --- Reject low score ---
        if score < 700:
            return (
                f"❌ Your credit score is {score}, below the required 700.\n"
                "Loan cannot be approved.",
                "complete"
            )

        # ==============================================================
        #  CASE 1: INSTANT APPROVAL  (NO SALARY SLIP NEEDED)
        # ==============================================================
        if requested_amount <= pre_limit:
            return (
                f"✅ Instant Approval!\n"
                f"Amount: ₹{requested_amount:,.0f}\n"
                f"Within your pre-approved limit (₹{pre_limit:,.0f}).\n"
                "Generating sanction letter...",
                "sanction"
            )

        # ==============================================================
        #  CASE 2: CONDITIONAL – SALARY SLIP REQUIRED
        #  Trigger the salary_slip stage HERE.
        # ==============================================================
        elif requested_amount <= 2 * pre_limit:

            # If salary slip already validated, compute EMI and compare to salary
            if customer.get("salary_slip_valid"):
                salary = customer.get("salary", 0)
                # Guard: if we do not have a salary value, request salary slip again
                if not salary or salary <= 0:
                    return (
                        "⚠️ Salary information is missing or invalid. Please provide a valid salary slip.",
                        "salary_slip"
                    )

                emi = calculate_emi(requested_amount, interest_rate, tenure_years)
                if emi <= 0.5 * salary:
                    return (
                        f"✅ Conditional approval after salary validation!\n"
                        f"Amount: ₹{requested_amount:,.0f} | Estimated EMI: ₹{emi:,.2f} | Salary: ₹{salary:,.0f}\n"
                        "Proceeding to sanction letter generation...",
                        "sanction"
                    )
                else:
                    return (
                        f"❌ EMI (₹{emi:,.2f}) exceeds 50% of your salary (₹{salary:,.0f}). Loan cannot be approved.",
                        "complete"
                    )

            # Tell frontend to request salary slip if not validated yet
            return (
                "Your requested amount exceeds your pre-approved limit.\n"
                "⚠️ To proceed further, we need your salary slip.\n"
                "Please upload your latest salary slip for EMI evaluation.",
                "salary_slip"         # <–––––––– KEY PART
            )

        # ==============================================================
        #  CASE 3: REJECTION – Amount exceeds 2× limit
        # ==============================================================
        return (
            f"❌ Requested amount ₹{requested_amount:,.0f} exceeds "
            f"2× your pre-approved limit (₹{2 * pre_limit:,.0f}).",
            "complete"
        )
