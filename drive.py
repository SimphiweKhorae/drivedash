# drive.py
from flask import Blueprint, session, jsonify, g
import sqlite3

drive_bp = Blueprint("drive", __name__)

# Helper function to get DB connection
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("users.db")
        g.db.row_factory = sqlite3.Row  # allows accessing columns by name
    return g.db

# Close DB connection after request
@drive_bp.teardown_app_request
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# ---------- Profile Route ----------
@drive_bp.route("/get_profile")
def get_profile():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    cur = db.execute("SELECT fullname, username, email, phone FROM users WHERE username=?", (session["user"],))
    user = cur.fetchone()

    if user:
        return jsonify({
            "fullname": user["fullname"],
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"]
        })
    else:
        return jsonify({"error": "User not found"}), 404
