import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization":  f"Bearer {OPENAI_API_KEY}"
}
data = {
    "model": "gpt-4.1-mini",
    "messages": [
        {"role": "user", "content": "Explain me globalization?"}
    ]
}

response = requests.post(url, headers=headers, json = data)

results = response.json()

print(results)