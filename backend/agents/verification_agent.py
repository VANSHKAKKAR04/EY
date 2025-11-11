from services.crm_api import get_customer_kyc
from services.credit_api import get_credit_score


class VerificationAgent:
    def perform_kyc(self, name: str, requested_amount: float = None):
        """
        Verify KYC details for a given customer and validate requested loan amount.

        Steps:
        1. Fetch KYC + credit info from CRM.
        2. Enrich missing data (credit score, preapproved limit).
        3. Compare requested loan with preapproved limit.
        4. Return formatted eligibility summary.
        """
        # --- Step 1: Fetch KYC data ---
        data = get_customer_kyc(name)
        if not data:
            return f"❌ KYC verification failed for '{name}'. Please recheck details or try again later."

        # --- Step 2: Ensure credit score is available ---
        data["credit_score"] = data.get("credit_score") or get_credit_score(name)
        pre_limit = data.get("preapproved_limit", 0)

        # --- Step 3: Loan request evaluation ---
        if requested_amount:
            if requested_amount <= pre_limit:
                eligibility_msg = (
                    f"✅ Requested amount ₹{requested_amount:,.0f} is within your "
                    f"pre-approved limit of ₹{pre_limit:,.0f}."
                )
            else:
                eligibility_msg = (
                    f"⚠️ Requested amount ₹{requested_amount:,.0f} exceeds your "
                    f"pre-approved limit of ₹{pre_limit:,.0f}.\n"
                    f"You may reapply for a smaller amount."
                )
        else:
            eligibility_msg = f"💡 Your pre-approved limit is ₹{pre_limit:,.0f}."

        # --- Step 4: Return formatted KYC summary ---
        return (
            f"KYC Verified ✅\n"
            f"Name: {data.get('name', 'N/A')}\n"
            f"City: {data.get('city', 'Unknown')}\n"
            f"Phone: {data.get('phone', 'N/A')}\n"
            f"Age: {data.get('age', 'N/A')}\n"
            f"Credit Score: {data['credit_score']}\n"
            f"Existing Loans: {data.get('existing_loans', 0)}\n"
            f"Preapproved Limit: ₹{pre_limit:,.0f}\n\n"
            f"{eligibility_msg}"
        )
