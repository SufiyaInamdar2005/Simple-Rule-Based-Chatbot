import os
import uuid
from collections import OrderedDict

from flask import Flask, jsonify, render_template, request, session

from chatbot import Chatbot
from llm import LLM

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

llm = LLM()
bots = OrderedDict()
MAX_SESSIONS = 500


def get_bot():
    sid = session.get("sid")
    if sid not in bots:
        sid = session["sid"] = uuid.uuid4().hex
        bots[sid] = Chatbot(llm)
        while len(bots) > MAX_SESSIONS:
            bots.popitem(last=False)
    return bots[sid]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/status")
def status():
    return jsonify(ai=llm.enabled)


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify(error="Message is required."), 400
    reply, done = get_bot().reply(message[:2000], data.get("timezone"))
    return jsonify(reply=reply, done=done)


@app.post("/reset")
def reset():
    bots.pop(session.get("sid"), None)
    session.clear()
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=int(os.getenv("PORT", 5000)))
