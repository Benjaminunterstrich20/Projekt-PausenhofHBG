import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "messages.json"

# Lade Nachrichten aus Datei
def load_messages():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Speichere Nachrichten in Datei
def save_messages(messages):
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f)

messages = load_messages()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if code:
            return redirect(url_for("chat", code=code))
    return render_template("index.html")

@app.route("/chat/<code>", methods=["GET", "POST"])
def chat(code):
    global messages
    if code not in messages:
        messages[code] = []

    # Keine Begrenzung mehr, jeder kann chatten
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            messages[code].append(msg)
            save_messages(messages)
        return redirect(url_for("chat", code=code))

    return render_template("chat.html", code=code, messages=messages[code])

if __name__ == "__main__":
    app.run(debug=True)
