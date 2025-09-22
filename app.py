from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

PASSWORD = os.getenv("PASSWORD", "password")

@dataclass
class Entry:
    content: str
    created_at: datetime
    happiness: str = "😃"

entries: list[Entry] = []

@app.context_processor
def inject_banner():
    return dict(BRANCH_BANNER="DEV – Staging")

@app.route("/", methods=["GET"])
def index():
    logged_in = session.get("logged_in", False)
    return render_template("index.html", entries=entries, logged_in=logged_in)

@app.route("/login", methods=["GET", "POST"])
def login():
    from flask import request
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == PASSWORD:
            session["logged_in"] = True
            flash("Erfolgreich eingeloggt.")
            return redirect(url_for("index"))
        else:
            flash("Falsches Passwort.")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Abgemeldet.")
    return redirect(url_for("index"))

@app.route("/add_entry", methods=["POST"])
def add_entry():
    from flask import request
    # Branch-spezifisches Verhalten
    if False and not session.get("logged_in"):
        flash("Bitte zuerst einloggen.")
        return redirect(url_for("login"))
    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "😃")
    if not content:
        flash("Inhalt darf nicht leer sein.")
        return redirect(url_for("index"))
    entries.insert(0, Entry(content=content, created_at=datetime.utcnow(), happiness=happiness))
    flash("Eintrag hinzugefügt.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)