from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import SanctionAgent

class MasterAgent:
    def __init__(self):
        self.sales = SalesAgent()
        self.verify = VerificationAgent()
        self.underwrite = UnderwritingAgent()
        self.sanction = SanctionAgent()
        self.state = {}

    def handle_message(self, msg):
        msg_lower = msg.lower()
        if "loan" in msg_lower:
            return self.sales.handle_sales(msg)
        elif "verify" in msg_lower:
            return self.verify.perform_kyc()
        elif "check" in msg_lower or "credit" in msg_lower:
            return self.underwrite.evaluate_loan()
        elif "sanction" in msg_lower:
            return self.sanction.generate_letter()
        else:
            return "Hello! I’m your Tata Capital AI assistant. Would you like to apply for a personal loan?"
