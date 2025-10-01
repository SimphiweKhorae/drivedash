# 🚖 DriveDash – Demo Ride-Hailing Login System

A simple **Flask-based login and dashboard system** built as a showcase exercise for an Uber-like ride-hailing platform.  
This project is **not production-ready**, but demonstrates user authentication, session handling, email confirmation, and a basic ride dashboard.

---

## ✨ Features
- 🔑 User **Registration** (with email, username, password, phone)  
- 📧 **Email confirmation** (via Gmail SMTP + tokens)  
- 🔐 User **Login & Logout** with sessions  
- 👤 Profile modal with user details  
- 📊 Simple dashboard (rides, nearby drivers, quick actions)  
- 🛠 SQLite database (`users.db`) for storing accounts  
- 📂 Organized with Flask **Blueprints**  

---

## 🗂 Project Structure
drivedash/
│── app.py # Main app entry point (handles auth + DB)
│── drive.py # Dashboard blueprint
│── users.db # SQLite database (auto-created)
│── templates/ # HTML templates
│ ├── index.html
│ ├── dashboard.html
│── static/ # CSS, JS, images
│ ├── css/
│ │ └── style.css
│ └── js/
└── README.md


2️⃣ Create and activate a virtual environment
-python -m venv venv
-source venv/bin/activate   # macOS/Linux
-venv\Scripts\activate      # Windows


3️⃣ Install dependencies
-pip install flask flask-mail itsdangerous


4️⃣ Configure Gmail for Email Confirmation
Open app.py and update these lines with your own Gmail address and a Gmail App Password:

-app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_app_password"

-⚠️ Important Notes:
Gmail requires you to create an App Password (not your normal Gmail password).
-Steps to generate:

Go to Google Account Security Settings.

Enable 2-Step Verification.

Under App Passwords, generate a new app password.

Use that password in place of your Gmail password in app.py.

5️⃣ Run the app
python app.py
The app will start on:http://127.0.0.1:5000/

