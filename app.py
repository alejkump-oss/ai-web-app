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

SYSTEM_PROMPT = """
You are an AI operating system.

You MUST always respond in valid JSON only.

Return one of these formats:

1) Answer:
{
  "type": "answer",
  "content": "short clear response"
}

2) Task:
{
  "type": "task",
  "title": "short title",
  "steps": ["step 1", "step 2", "step 3"]
}

RULES:
- ONLY JSON
- NO markdown
- NO extra text
- If user is unclear, still respond with type=answer
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")

        if not user_input:
            return jsonify({
                "type": "answer",
                "content": "No input provided"
            })

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()

        # SAFE JSON PARSE
        try:
            data = json.loads(reply)
        except Exception:
            data = {
                "type": "answer",
                "content": reply
            }

        messages.append({"role": "assistant", "content": reply})

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "type": "answer",
            "content": f"Server error: {str(e)}"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
