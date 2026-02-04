"""
Flask Portfolio App
Author: Spencer Renfro
Date: 2026-1-29
"""
from flask import Flask, render_template, request, url_for, redirect
from passlib.hash import sha256_crypt
from datetime import datetime
import json


app = Flask(__name__)
USERS_FILE = "static/data/users.json"

# Helper functions

@app.context_processor
def inject_now():
    return {"now": datetime.now()}

    # Load users from JSON file
def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
    # Save users to JSON file
def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data,f, indent=4)
        
    # Check if username exists

def check_username_exists(username, email):
    users = load_users()
    for user in users["users"]:
        if user["username"].lower() == username.lower() or user["email"].lower() == email.lower():
            return True
    return False

def authenticate_user(username_or_email, password):
    users = load_users()
    for user in users["users"]:
        if user["username"].lower() == username_or_email.lower() or user["email"].lower() == username_or_email.lower():
            stored_password = user["password"]
            if stored_password.startswith("$5$"):
                if sha256_crypt.verify(password, stored_password):
                    return user
            elif stored_password == password:
                return user
    return None
# Routes
@app.route("/")
def index():
    now = datetime.now()
    return render_template("index.html", now=now)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='world'):
    return render_template('hello.html', name=name)

@app.route("/polytopia")
def polytopia():
    return render_template('polytopia.html')

@app.route("/steamaction")
def steamaction():
    return render_template('steamaction.html')

@app.route("/inventory_management")
def inventory_management():
    return render_template('inventory_management.html')

@app.route("/user_homepage/<username>")
def user_homepage(username):
    return render_template("user_homepage.html", username=username)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method =="GET":
        return render_template('signup.html')
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not username or not email or not password:
        return render_template('signup.html', error="Please fill out all fields")
    
    data = load_users()
    
    # Check for existing username
    if check_username_exists(username, email):
        return render_template('signup.html', error="Username or email already registered")
    
    # Hash password
    hash_password = sha256_crypt.hash(password)
    
    # call to compare the two entries
    if sha256_crypt.verify(password, hash_password):
        print("Password matches")

    # Create new user
    data["users"].append({
        "username" : username,
        "email" : email,
        "password" : hash_password,
        "unhased_password" : password
    })
    save_users(data)
    print("User created:", username, email, password)
    
    return redirect(url_for('index'))

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if username and password:
        user = authenticate_user(username, password)
        if user:
            return redirect(url_for('user_homepage', username=user["username"]))

    return render_template("login.html")


@app.route("/update_password", methods=["POST"])

def update_password():
    username = request.form.get("username")
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    
    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            if sha256_crypt.verify(current_password, user["password"]):
                user["password"] = sha256_crypt.hash(new_password)
                user["unhased_password"] = new_password
                save_users(data)
                return redirect(url_for('index.html'))
            return render_template("user_homepage.html", username=username, error="Current password is incorrect.")
    return render_template("user_homepage.html", username=username, error="User not found.")


        
print("Hello from app.py")
if __name__ == "__main__":
    app.run(debug=True)
