import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self, data_path: str):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []
        self.load_data(data_path)

    def load_data(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)

        chunks = []

        # ✅ Support both list and dict formats
        if isinstance(data, list):
            # List of customer records
            for customer in data:
                name = customer.get("name", "Unknown")
                city = customer.get("city", "Unknown")
                pre_limit = customer.get("pre_approved_limit", "N/A")
                requested = customer.get("requested_loan", "N/A")
                chunks.append(
                    f"Customer {name} from {city} has a pre-approved limit of ₹{pre_limit} "
                    f"and requested a loan of ₹{requested}."
                )

        elif isinstance(data, dict):
            # Dictionary of name → details
            for name, info in data.items():
                city = info.get("city", "Unknown")
                pre_limit = info.get("pre_approved_limit", "N/A")
                requested = info.get("requested_loan", "N/A")
                chunks.append(
                    f"Customer {name} from {city} has a pre-approved limit of ₹{pre_limit} "
                    f"and requested a loan of ₹{requested}."
                )

        # Add business/policy facts
        chunks += [
            "Credit score above 700 qualifies for instant approval.",
            "Loans above 2× pre-approved limit require salary slip verification.",
            "KYC must include phone, address, and PAN verification."
        ]

        self.text_chunks = chunks

        # Build FAISS index
        embeddings = self.model.encode(chunks)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype("float32"))
        print(f"✅ RAG index built with {len(chunks)} entries.")

    def retrieve(self, query: str, k=3):
        query_emb = self.model.encode([query])
        D, I = self.index.search(np.array(query_emb).astype("float32"), k)
        return [self.text_chunks[i] for i in I[0]]
