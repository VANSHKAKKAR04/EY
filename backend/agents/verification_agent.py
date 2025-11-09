from services.crm_api import get_customer_kyc

class VerificationAgent:
    def perform_kyc(self):
        data = get_customer_kyc("Ravi Kumar")  # dummy lookup
        if data:
            return f"KYC verified for {data['name']} from {data['city']}."
        return "Unable to verify KYC — please recheck your details."
