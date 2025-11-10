from services.crm_api import get_customer_kyc
from services.credit_api import get_credit_score

class VerificationAgent:
    def perform_kyc(self, name: str, requested_amount: float = None):
        """Verify KYC details and validate requested loan amount."""
        data = get_customer_kyc(name)
        if not data:
            return f"❌ KYC verification failed for {name}. Please recheck details."

        # Generate credit score if missing
        if "credit_score" not in data:
            data["credit_score"] = get_credit_score(name)

        preapproved_limit = data.get("preapproved_limit", 0)

        # --- Determine eligibility based on request ---
        eligibility_msg = ""
        if requested_amount:
            if requested_amount <= preapproved_limit:
                eligibility_msg = (
                    f"✅ Requested amount ₹{requested_amount:,.0f} is within your "
                    f"pre-approved limit of ₹{preapproved_limit:,.0f}."
                )
            else:
                eligibility_msg = (
                    f"⚠️ Requested amount ₹{requested_amount:,.0f} exceeds your "
                    f"pre-approved limit of ₹{preapproved_limit:,.0f}. "
                    f"You may reapply for a smaller amount."
                )
        else:
            eligibility_msg = f"💡 Your pre-approved limit is ₹{preapproved_limit:,.0f}."

        # --- Final summary ---
        return (
            f"KYC verified ✅\n"
            f"Name: {data['name']}\n"
            f"City: {data['city']}\n"
            f"Phone: {data['phone']}\n"
            f"Credit Score: {data['credit_score']}\n"
            f"Preapproved Limit: ₹{preapproved_limit:,.0f}\n\n"
            f"{eligibility_msg}"
        )
