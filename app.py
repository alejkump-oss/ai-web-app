import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY ni nastavljen!")

client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": """
You are an AI operating system.

IMPORTANT RULE:
You MUST respond ONLY in valid JSON.
No text before or after JSON.

You have two modes:

1) TASK mode:
{
  "type": "task",
  "title": "short title",
  "steps": ["step 1", "step 2", "step 3"]
}

2) ANSWER mode:
{
  "type": "answer",
  "content": "short clear answer"
}

RULES:
- NEVER write normal text
- NEVER use markdown
- ALWAYS return valid JSON
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
except:
    data = {
        "type": "answer",
        "content": reply}
        messages.append({"role": "assistant", "content": reply})

        return jsonify(data)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)