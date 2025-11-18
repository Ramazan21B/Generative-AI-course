import json, os, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

CHAT_URL = f"{BASE_URL}/chat/completions"

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

SYSTEM_PROMPT = ("You are a helpful math tutor. You assist students with understanding and helping them solve math problems step-by-step. "
                 "Always encourage students to think critically and explain concepts clearly."
                 " When providing solutions, break down the steps and explain the reasoning behind each step.")


def get_math_tutor_response(user_message: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }
    try:
        response = requests.post(
            CHAT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"An error occurred while contacting the API: {e}"
    
def main():
    print("Welcome to the Math Tutor!")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("Enter your math question: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = get_math_tutor_response(user_input)
        print("Math Tutor:", response)

if __name__ == "__main__":
    main()
