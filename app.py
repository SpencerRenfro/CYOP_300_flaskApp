"""
Flask Portfolio App
Author: Spencer Renfro
Date: 2026-1-29
"""
from datetime import datetime
import json
from flask import Flask, render_template, request, url_for, redirect
from passlib.hash import sha256_crypt


app = Flask(__name__)
USERS_FILE = "static/data/users.json"

# Helper functions

def password_strength_check(password):
    """
        This function tests password strength.
    """
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase character"
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase character"
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number"
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return "Password must contain at least one special character"
    return None
@app.context_processor
def inject_now():
    """
    Injects the current date and time into all templates.
    """
    return {"now": datetime.now()}


def load_users():
    """
    Loads users from the JSON file.
    """
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data):
    """
    Saves users to the JSON file.
    """
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data,f, indent=4)



def check_username_exists(username, email):
    """
    Checks if a username or email already exists in the user database.
    """
    users = load_users()
    for user in users["users"]:
        if user["username"].lower() == username.lower() or user["email"].lower() == email.lower():
            return True
    return False


def authenticate_user(username_or_email, password):
    """
    Authenticates a user by checking the username/email 
    and password against the user database.
    """
    users = load_users()
    for user in users["users"]:
        if (
            user["username"].lower() == username_or_email.lower() or
            user["email"].lower() == username_or_email.lower()
        ):
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
    """
    Renders the index page.
    """
    now = datetime.now()
    return render_template("index.html", now=now)



@app.route("/polytopia")
def polytopia():
    """
    Renders the polytopia page.
    """
    return render_template('polytopia.html')


@app.route("/steamaction")
def steamaction():
    """
    Renders the steamaction page.
    """
    return render_template('steamaction.html')



@app.route("/inventory_management")
def inventory_management():
    """
    Renders the inventory management page.
    """
    return render_template('inventory_management.html')


@app.route("/user_homepage/<username>")
def user_homepage(username):
    """
    Renders the user homepage.
    """
    return render_template("user_homepage.html", username=username)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles user signup.
    """

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

    # Check password strength
    error = password_strength_check(password)
    if error:
        return render_template('signup.html', error=error)


    # Hash password
    hash_password = sha256_crypt.hash(password)

    # call to compare the two entries
    if sha256_crypt.verify(password, hash_password):
        print("Password matches")

    # Create new user
    data["users"].append({
        "username" : username,
        "email" : email,
        "password" : hash_password
    })
    save_users(data)
    print("User created:", username, email, password)

    return redirect(url_for('index'))


@app.route("/login", methods=["GET"])
def login():
    """
    Handles user login.
    """
    username = request.args.get("username")
    password = request.args.get("password")
    if username and password:
        user = authenticate_user(username, password)
        if user:
            return redirect(url_for('user_homepage', username=user["username"]))

    return render_template("login.html")


@app.route("/update_password", methods=["POST"])

def update_password():
    """
    This function will update the password for a user.
    """
    username = request.form.get("username")
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")

    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            if sha256_crypt.verify(current_password, user["password"]):
                if sha256_crypt.verify(new_password, user["password"]):
                    return render_template(
                        "user_homepage.html",
                        username=username,
                        error="New password cannot be the same as current password."
                    )

                # Check password strength,
                # if error returns error message string stored in error
                error = (
                    password_strength_check(new_password)
                    )
                if error:
                    return render_template(
                        "user_homepage.html",
                        username=username,
                        error=error
                    )
                user["password"] = sha256_crypt.hash(new_password)
                save_users(data)
                return redirect(url_for('index'))
            return render_template(
            "user_homepage.html",
            username=username,
            error="Current password is incorrect."
        )
    return render_template("user_homepage.html", username=username, error="User not found.")



if __name__ == "__main__":
    app.run(debug=True)
