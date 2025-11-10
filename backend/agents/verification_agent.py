from services.crm_api import get_customer_kyc
from services.credit_api import get_credit_score  # import your credit score helper

class VerificationAgent:
    def perform_kyc(self, name: str):
        """Verify KYC details for a given customer name."""
        data = get_customer_kyc(name)
        if not data:
            return f"❌ KYC verification failed for {name}. Please recheck details."

        # Generate credit score if missing
        if "credit_score" not in data:
            data["credit_score"] = get_credit_score(name)

        # Return formatted summary
        return (
            f"KYC verified ✅\n"
            f"Name: {data['name']}\n"
            f"City: {data['city']}\n"
            f"Phone: {data['phone']}\n"
            f"Credit Score: {data['credit_score']}\n"
            f"Preapproved Limit: ₹{data['preapproved_limit']}"
        )
