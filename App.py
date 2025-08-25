from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database checked/created successfully")
# --- SIGNUP ROUTE ---
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor=conn.cursor()
      

        # Check if username OR email already exists
        cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "⚠️ Username or Email already exists! Please try another."

        # Insert new user
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
        conn.close()

        return redirect("http://127.0.0.1:5000/login")

    return render_template("signup.html")
    
    # ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")  # Make sure this file exists in /templates

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Store username in session (optional)
            session["user"] = username
            # Redirect to index page after successful login
            return redirect("http://127.0.0.1:5000/")  # Works on Android
        else:
            return "❌ Invalid username or password! Please try again."

    return render_template("login.html")

@app.route("/donation")
def donation():
    return render_template("Dlist.html")
  
@app.route("/requests")
def requests():
    return render_template("Rlist.html")
   
# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"<h1>Welcome {session['user']}!</h1><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for("login"))

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))

# ---------- RUN APP ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)