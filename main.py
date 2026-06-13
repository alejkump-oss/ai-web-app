from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "Ti si prijazen pomočnik, ki odgovarja kratko in jasno."}
]

print("AI chatbot je pripravljen. Za izhod napiši 'exit'.\n")

while True:
    user_input = input("Ti: ")

    if user_input.lower() == "exit":
        print("Chatbot končan 👋")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    print("AI:", reply)

    messages.append({"role": "assistant", "content": reply})
