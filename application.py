import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///homecook.db")


# Home page for search
@app.route("/")
def index():

    # Display all foods in database to be selected
    food = db.execute("SELECT * FROM food")

    # Render search page
    return render_template("index.html", food=food)


# Display search results
@app.route("/search", methods=["GET", "POST"])
def search():

    # If search submitted then process query
    if request.method == "POST":

        # Form is received as an array of dictionaries
        query = request.form

        # Define array of choices
        choices = []

        # Iterate every value in query to add to array
        for value in query.values():
            split = value.split(',')
            for i in split:
                food = i.strip()
                choices.append(food)

        # Stay on search page if nothing selected / typed
        if not choices:
            return redirect("/")

        # Convert array to string insertable into database query
        string = ''

        # Iterate through each choice and add formatting items for query
        for i in choices:
            string += "food_name LIKE ('%"
            string += i
            string += "%') OR "

        # Last OR is not needed
        string = string[:-4]

        # Search database for recipes containing only those choices
        recipes = db.execute(f"SELECT * FROM recipes WHERE recipe_id NOT IN (SELECT recipe_id FROM ingredients WHERE food_id NOT IN (SELECT food_id FROM food WHERE {string}))")

        # If no results, render no result message
        if not recipes:
            return render_template("noresults.html")

        # Render results
        return render_template("results.html", recipes=recipes)

    # If used GET then redirect to search page
    else:
        return redirect("/")


# Save Process
@app.route("/saved", methods=["GET", "POST"])
@login_required
def saved():
    """Save Recipe"""

    if not session["user_id"]:
        return redirect("/")

    else:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            # Enter save into saved table
            recipe_id = request.form.get("recipe-id")
            db.execute("INSERT INTO saved VALUES (?, ?)", session["user_id"], recipe_id)

        # Retrieve user's saved recipes
        recipes = db.execute("SELECT * FROM recipes WHERE recipe_id IN (SELECT recipe_id FROM saved WHERE user_id = ?)", session["user_id"])

        return render_template("saved.html", recipes=recipes)


# Delete Process
@app.route("/delete", methods=["GET", "POST"])
def delete():
    """Delete Recipe"""

    if request.method == "POST":

        # Delete recipe from saved table
        recipe_id = request.form.get("recipe-id")
        db.execute("DELETE FROM saved WHERE user_id = ? AND recipe_id = ?", session["user_id"], recipe_id)

        # Retrieve new list of user's saved recipes
        recipes = db.execute("SELECT * FROM recipes WHERE recipe_id IN (SELECT recipe_id FROM saved WHERE user_id = ?)", session["user_id"])

        return render_template("saved.html", recipes=recipes)

    else:
        return redirect("/")


# Login Process
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Logout process
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


# Password requirements: need to have some number of letters, numbers, and/or symbols
def check_password(password):
    # Define special characters
    special = ['!', '@', '#', '$', '%', '?']

    # At least 8 digits
    if len(password) < 8:
        return False

    # At most 20 digits
    elif len(password) > 20:
        return False

    # "any" function from https://www.w3schools.com/python/ref_func_any.asp

    # Contains at least 1 number
    elif not any(char.isdigit() for char in password):
        return False

    # Contains at least 1 uppercase letter
    elif not any(char.isupper() for char in password):
        return False

    # Contains at least 1 lowercase letter
    elif not any(char.islower() for char in password):
        return False

    # Contains at least 1 special character
    elif not any(char in special for char in password):
        return False

    # All requirements met
    return True


# Register process
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password meets requirements
        password = request.form.get("password")
        if not check_password(password):
            return apology("password requirements not met")

        # Ensure password and confirmation match
        if password != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("username already exists")

        # Hash password using generate_password_hash
        password_hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Add hashed password to database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), password_hash)

        # Automatically log in user
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# Error handling process
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
