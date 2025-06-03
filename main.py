from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Nachrichten pro Code speichern (einfach in RAM)
messages = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if code:
            return redirect(url_for("chat", code=code))
    return render_template("index.html")

@app.route("/chat/<code>", methods=["GET", "POST"])
def chat(code):
    if code not in messages:
        messages[code] = []

    # Maximal 2 Nachrichten pro Raum (2 Personen)
    has_sent = len(messages[code]) >= 2

    if request.method == "POST" and not has_sent:
        msg = request.form.get("message", "").strip()
        if msg:
            messages[code].append(msg)
        return redirect(url_for("chat", code=code))

    return render_template("chat.html", code=code, messages=messages[code], has_sent=has_sent)

if __name__ == "__main__":
    app.run(debug=True)
