from services.mistral_api import query_mistral
from services.rag_service import RAGService

class SalesAgent:
    def __init__(self, data_path="./data/customers.json"):
        self.rag = RAGService(data_path)

    def handle_sales(self, user_message: str):
        # Step 1: Retrieve context from RAG
        context_docs = self.rag.retrieve(user_message)
        context_text = "\n".join(context_docs)

        # Step 2: Construct grounded prompt
        prompt = f"""
        You are a friendly Tata Capital Sales Assistant helping customers with personal loans.
        Use the following context when answering:

        Context:
        {context_text}

        Customer says: "{user_message}"

        Respond naturally, mention relevant offers or next steps, and stay factual.
        """

        return query_mistral(prompt)
