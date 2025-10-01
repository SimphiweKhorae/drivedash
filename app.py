from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import sqlite3

# Import and register blueprint
from drive import drive_bp
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- Flask-Mail Configuration ----------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"  # change to your email
app.config["MAIL_PASSWORD"] = "app password"         # change to your app password

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        is_confirmed INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

init_db()

app.register_blueprint(drive_bp)

# ---------- Home Page ----------
@app.route("/")
def index():
    return render_template("index.html")

# ---------- Register Route ----------
@app.route("/register", methods=["POST"])
def register():
    fullname = request.form["fullname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    phone = request.form["phone"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (fullname, email, username, password, phone) VALUES (?, ?, ?, ?, ?)",
                  (fullname, email, username, password, phone))
        conn.commit()
        conn.close()

        # Send email confirmation
        token = serializer.dumps(email, salt="email-confirm")
        confirm_url = url_for("confirm_email", token=token, _external=True)
        msg = Message("Confirm Your Account", sender=app.config["MAIL_USERNAME"], recipients=[email])
        msg.body = f"Hello {fullname},\n\nPlease confirm your account by clicking the link:\n{confirm_url}\n\nThis link expires in 30 minutes."
        mail.send(msg)

        flash("Registration successful! Check your email to confirm your account.", "success")
    except sqlite3.IntegrityError:
        flash("Email or username already exists.", "danger")

    return redirect(url_for("index"))

# ---------- Login Route ----------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        if user[-1] == 0:  # is_confirmed column
            flash("Please confirm your email before logging in.", "warning")
            return redirect(url_for("index"))
        else:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))  # redirect to dashboard after login
    else:
        flash("Invalid username or password.", "danger")
        return redirect(url_for("index"))

# ---------- Email Confirmation ----------
@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=1800)
    except SignatureExpired:
        flash("The confirmation link has expired.", "danger")
        return redirect(url_for("index"))
    except BadSignature:
        flash("Invalid confirmation link.", "danger")
        return redirect(url_for("index"))

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_confirmed=1 WHERE email=?", (email,))
    conn.commit()
    conn.close()

    flash("Email confirmed! You can now log in.", "success")
    return redirect(url_for("index"))

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("index"))
    username = session["user"]
    return render_template("dashboard.html", username=username)

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
