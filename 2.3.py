import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=API_KEY)

with open("bot_qa.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

def ask_llm(user_q: str) -> str:
    faq_text = "\n".join(
        [f"Вопрос: {item['q']}\nОтвет: {item['a']}" for item in faqs]
    )

    prompt = f"""
Ты — полезный AI-ассистент банка. У тебя есть список часто задаваемых вопросов и ответов (FAQ).

Клиент задаёт вопрос: {user_q}

Задача:
1. Найди наиболее похожий вопрос из FAQ.
2. Если нашёл — ответь строго текстом ответа.
3. Если подходящего вопроса нет — ответь:
"Извините, я не могу помочь с этим вопросом. Обратитесь, пожалуйста, к нашему специалисту."

Вот список FAQ:
{faq_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Ты — AI-бот-консультант банка."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content.strip()


def get_bot_response(user_input: str) -> str:
    answer = ask_llm(user_input)
    if "извините, я не могу помочь" in answer.lower():
        return "Извините, я не могу помочь с этим вопросом. Обратитесь, пожалуйста, к нашему специалисту."
    return answer


def main():
    print("Сейчас с вами работает AI-бот на базе OpenAI:", MODEL)
    while True:
        user_input = input("Введите ваш вопрос (или 'exit'): ").strip()
        if user_input.lower() in ("exit"):
            print("Спасибо за использование AI-бота. До свидания!")
            break
        print("AI-бот:", get_bot_response(user_input))


if __name__ == "__main__":
    main()
