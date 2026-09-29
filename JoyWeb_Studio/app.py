import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET")
DB_NAME = os.environ.get("DB_NAME", "joyweb.db")

BUSINESS = {
    "name": "JoyWeb Studio",
    "location": "Ngozi, Burundi",
    "phone": "67 540 344",
    "whatsapp": "25771223440"
}

SERVICES = [
    ("Business Website", "Modern responsive websites for companies and organizations.", "From 250,000 BIF"),
    ("E-commerce Website", "Online shops with products, customers, orders and payment-ready architecture.", "From 600,000 BIF"),
    ("Hotel Management System", "Rooms, reservations, customers, payments and reports.", "From 900,000 BIF"),
    ("Restaurant Management System", "Tables, menu, orders, sales and reports.", "From 900,000 BIF"),
    ("Portfolio Website", "Professional personal or company portfolio.", "From 200,000 BIF"),
    ("Custom Software", "Software designed around the client's workflow.", "Quotation")
]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_NAME)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    db = sqlite3.connect(DB_NAME)
    db.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            service TEXT NOT NULL,
            budget TEXT,
            details TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_business():
    return {"business": BUSINESS}

@app.route("/")
def home():
    return render_template("index.html", services=SERVICES)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if request.form.get("website"):
            return redirect(url_for("contact"))

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        budget = request.form.get("budget", "").strip()
        details = request.form.get("details", "").strip()

        if not name or not phone or not service or not details:
            flash("Please fill in all required fields.", "error")
            return render_template("contact.html", services=SERVICES)

        db = get_db()
        db.execute(
            "INSERT INTO leads (name,phone,email,service,budget,details) VALUES (?,?,?,?,?,?)",
            (name, phone, email, service, budget, details)
        )
        db.commit()
        flash("Project request sent successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", services=SERVICES)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == os.environ.get("ADMIN_PASSWORD", "1234"):
            session["admin"] = True
            return redirect(url_for("admin_leads"))
        flash("Incorrect password.", "error")
    return render_template("admin/login.html")

@app.route("/admin/leads")
@admin_required
def admin_leads():
    leads = get_db().execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    return render_template("admin/leads.html", leads=leads)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5003)), debug=True)
