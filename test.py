import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": "Ты мой личный ассистент в чате телеграмм, ты анализируешь текст, поведение человека по тексту, и др аспекты в общений."},
        {
            "role": "user",
            "content": "Привет как дела?"
        }
    ]
)

print(completion.choices[0].message)
