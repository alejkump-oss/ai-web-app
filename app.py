from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY ni nastavljen!")

client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": """
You are an AI operating system.

You MUST always respond in valid JSON.

Two modes:

1) TASK:
{
  "type": "task",
  "title": "short title",
  "steps": ["step 1", "step 2", "step 3"]
}

2) ANSWER:
{
  "type": "answer",
  "content": "short clear response"
}

RULES:
- ONLY JSON
- NO markdown
- NO extra text
"""
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()

        try:
            data = json.loads(reply)
        except Exception:
            data = {
                "type": "answer",
                "content": reply,
                "error": "invalid_json_from_model"
            }

        messages.append({"role": "assistant", "content": reply})

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
