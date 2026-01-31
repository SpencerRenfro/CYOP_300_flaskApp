"""
Flask Portfolio App
Author: Spencer Renfro
Date: 2026-1-29
"""
from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import json


app = Flask(__name__)
USERS_FILE = "static/data/users.json"

# Helper functions

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
        if user["username"].lower() == username.lower() or user["email"].lower() == username.lower():
            return True
    return False

def check_password(username, email, password):
    users = load_users()
    for user in users["users"]:
        if user["username"].lower() == username.lower() or user["email"].lower() == username.lower():
            if user["password"] == password:
                return True
    return False
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
    
    # Create new user
    data["users"].append({
        "username" : username,
        "email" : email,
        "password" : password
    })
    save_users(data)
    print("User created:", username, email, password)
    
    return redirect(url_for('index'))

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")
    
    if username and password:
        if  check_password(username, email, password):
            return redirect(url_for('user_homepage', username=username))

    return render_template("login.html")

        
print("Hello from app.py")
if __name__ == "__main__":
    app.run(debug=True)
