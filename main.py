import os
import openai
from flask import Flask, request
import requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"]["text"]

    reply = ask_gpt(user_message)

    requests.post(URL, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == "__main__":
    app.run()
