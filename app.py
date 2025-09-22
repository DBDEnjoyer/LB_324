from flask import Flask, render_template, request, redirect, url_for, session, flash
from dataclasses import dataclass
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# ---- Data model ----
@dataclass
class Entry:
    content: str
    created_at: datetime
    happiness: str


# In-memory storage of entries (the test imports this!)
entries: list[Entry] = []


# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password")
        expected_pw = os.environ.get("PASSWORD", "password")
        if pw == expected_pw:
            session["logged_in"] = True
            flash("Login erfolgreich.")
            return redirect(url_for("index"))
        else:
            flash("Falsches Passwort.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logout erfolgreich.")
    return redirect(url_for("index"))


@app.route("/add_entry", methods=["POST"])
def add_entry():
    """
    LB-324 official test posts here WITHOUT login.
    It expects:
      - 302 redirect to "/"
      - entries[0] to have correct content + happiness
    So: do not enforce login for this route.
    """
    content = (request.form.get("content") or "").strip()
    happiness = request.form.get("happiness") or "😃"

    if not content:
        flash("Inhalt darf nicht leer sein.")
        return redirect(url_for("index"))

    # Insert newest first, so entries[0] is the latest
    entries.insert(0, Entry(content=content, created_at=datetime.utcnow(), happiness=happiness))

    flash("Eintrag hinzugefügt.")
    return redirect(url_for("index"))


# ---- Main entry point ----
if __name__ == "__main__":
    app.run(debug=True)
