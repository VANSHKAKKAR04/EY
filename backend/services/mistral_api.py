import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.mistral.ai/v1/chat/completions"

def query_mistral(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral-medium",   # or mistral-small / large / open-mixtral
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error from Mistral:", e, response.text)
        return "⚠️ Error fetching response from Mistral API."
