# A simple TODO app that lets you add TODO items and check them off, hopefully helping your productivity
# This project helped me learn a lot about JQuery, Ajax and Flask
# Updated to include a "Goals" tab which I had wanted from the start

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import re
from redissession import RedisSessionInterface
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, get_datetime


# Configure application
app = Flask(__name__)
app.session_interface = RedisSessionInterface()

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

# Configure CS50 Library to use database
db = SQL("postgres://dnedntjbatoqvz:2f5809d29929f230992bc3a295b31dcf2c65497274b44cc3145e4b364f6b28d0@ec2-75-101-138-26.compute-1.amazonaws.com:5432/d4obbeungvdjk8")


@app.route("/")
@login_required
def index():
    """Show reminders"""

    reminders = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])

    users = db.execute("SELECT * FROM users WHERE id = :user_id",
                       user_id=session["user_id"])

    firstname = users[0]["firstname"]

    return render_template("index.html", reminders=reminders, name=firstname)


@app.route("/goals")
@login_required
def goals():
    """Show goals"""

    goals = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                       user_id=session["user_id"])

    return render_template("goals.html", goals=goals)


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

        # User reached route via POST (as by submitting a form via POST)
        users = db.execute("SELECT * FROM users WHERE username = :username",
                           username=request.form.get("username"))
        print(users, "users")
        print(len(users), "len(users)")
        print(check_password_hash(users[0]["password"], request.form.get("password")), 'check_password_hash(users[0]["password"], request.form.get("password"))')


        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Forget any user_id
        session.clear()

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure all fields are filled
        if not firstname:
            return apology("Missing first name!")
        elif not username:
            return apology("Missing username!")
        elif not email:
            return apology("Missing email!")
        elif not password:
            return apology("Missing password!")
        elif not confirmation:
            return apology("Missing password confirmation!")

        # Ensure password matches confirmation
        elif password != confirmation:
            return apology("Password and confirmation do not match!")

        # Hash password
        password = generate_password_hash(password)

        # Ensure username is unique
        username_check = db.execute("SELECT * FROM users WHERE username = :username",
                                    username=username)
        if username_check:
            return apology("Username taken, please select different username")

        # Add user to database

        db.execute("INSERT INTO users (firstname, lastname, email, username, password, datetime) VALUES (:firstname, :lastname, :email, :username, :password, :datetime)",
                   firstname=firstname, lastname=lastname, email=email, username=username, password=password, datetime=get_datetime())

        # Automatically login user
        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = :username",
                           username=username)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Alert
        flash("Welcome to Done&Done!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_confirmation = request.form.get("new_confirmation")

        # Ensure all fields are filled
        if not old_password:
            return apology("Missing old password!")

        # Hash old password
        hashed_old_password = generate_password_hash(old_password)
        print(hashed_old_password)

        # Query database for users
        users = db.execute("SELECT * FROM users WHERE id = :user_id",
                           user_id=session["user_id"])

        print(users[0]["password"])

        # Ensure old password is correct
        if not check_password_hash(users[0]["password"], old_password):
            return apology("Incorrect password!")

        # Ensure other fields are filled
        elif not new_password:
            return apology("Missing new password!")
        elif not new_confirmation:
            return apology("Missing new password confirmation!")

        # Ensure password matches confirmation
        elif new_password != new_confirmation:
            return apology("Password and confirmation do not match!")

        # Hash new password
        hashed_new_password = generate_password_hash(new_password)
        print(hashed_new_password)

        # Ensure new password is not same as old password
        if check_password_hash(users[0]["password"], new_password):
            return apology("New password matches current password, please enter different password!")

        # Change password
        db.execute("UPDATE users set password = :hashed_new_password WHERE id = :user_id",
                   hashed_new_password=hashed_new_password, user_id=session["user_id"])

        # Flash message
        flash("Password change successful!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """Create New Reminder"""
    if request.method == "POST":

        reminder = request.form.get("reminder")
        details = request.form.get("details")

        if not reminder:
            return apology("Missing Reminder")

        # Insert reminder
        db.execute("INSERT INTO reminders (name, details, user_id, datetime) VALUES (:reminder, :details, :user_id, :datetime)",
                   reminder=reminder, details=details, user_id=session["user_id"], datetime=get_datetime())

        return redirect("/")

    else:
        return render_template("new.html")


@app.route("/new_goal", methods=["GET", "POST"])
@login_required
def new_goal():
    """Create New Goal"""
    if request.method == "POST":

        goal = request.form.get("goal")
        details = request.form.get("details")

        if not goal:
            return apology("Missing Goal")

        # Insert reminder
        db.execute("INSERT INTO goals (name, details, user_id, datetime) VALUES (:goal, :details, :user_id, :datetime)",
                   goal=goal, details=details, user_id=session["user_id"], datetime=get_datetime())

        return redirect("/goals")

    else:
        return render_template("new_goal.html")


@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    """Show completed tasks"""
    if request.method == "POST":

        # Clear completed
        db.execute("DELETE FROM completed WHERE user_id = :user_id",
                   user_id=session["user_id"])
        flash("Cleared all completed tasks!")
        return redirect("/completed")

    else:
        completed = db.execute("SELECT * FROM completed WHERE user_id = :user_id",
                               user_id=session["user_id"])

        return render_template("completed.html", completed=completed)


@app.route("/lists/new_list", methods=["GET", "POST"])
@login_required
def new_list():
    """Create New List"""
    if request.method == "POST":

        list_name = request.form.get("list")
        details = request.form.get("details")

        if not list_name:
            return apology("Missing List")

        # Insert list
        db.execute("INSERT INTO lists (name, details, user_id, datetime) VALUES (:list_name, :details, :user_id, :datetime)",
                   list_name=list_name, details=details, user_id=session["user_id"], datetime=get_datetime())

        return redirect("/lists")

    else:
        return render_template("new_list.html")


@app.route("/lists/new_item", methods=["GET", "POST"])
@login_required
def new_item():
    """Create New Item"""
    if request.method == "POST":

        item_name = request.form.get("item")
        details = request.form.get("details")
        list_id = request.form.get("list")

        if not item_name:
            return apology("Missing Item")
        elif not list_id:
            return apology("Missing list")

        # Insert reminder
        db.execute("INSERT INTO items (name, details, user_id, list_id, datetime) VALUES (:item_name, :details, :user_id, :list_id, :datetime)",
                   item_name=item_name, details=details, user_id=session["user_id"], list_id=list_id, datetime=get_datetime())

        return redirect("/lists")

    else:
        lists = db.execute("SELECT * FROM lists WHERE user_id = :user_id",
                           user_id=session["user_id"])
        return render_template("new_item.html", lists=lists)


@app.route('/lists/delete', methods=["GET", "POST"])
@login_required
def delete_list():
    """Delete entire list (Including items within)"""
    if request.method == "POST":
        list_id = request.form.get("list")

        if not list_id:
            return apology("Missing list")

        # Delete all list items
        db.execute("DELETE FROM items WHERE list_id = :list_id",
                   list_id=list_id)

        # Delete list
        db.execute("DELETE FROM lists WHERE id = :list_id",
                   list_id=list_id)
        return redirect("/lists")

    else:
        # Get lists
        lists = db.execute("SELECT * FROM lists WHERE user_id = :user_id",
                           user_id=session["user_id"])

        return render_template("delete_list.html", lists=lists)


@app.route('/lists', methods=["GET", "POST"])
@login_required
def list_page():
    """GET: Show list names,
       POST: show checkale list items of respective list"""
    if request.method == 'POST':
        list_id = request.form.getlist("check_list")
        list_id = list_id[0]
        print(list_id, "list_id")
        # Get list ID from form submission
        items = db.execute("SELECT * FROM items WHERE list_id = :list_id",
                           list_id=list_id)
        print(jsonify(items), "jsonify(items)")
        return jsonify(items)

    else:
        lists = db.execute("SELECT * FROM lists WHERE user_id = :user_id",
                           user_id=session["user_id"])

        return render_template("lists.html", lists=lists)

# ========================AJAX CALLS========================


@app.route("/checked_item", methods=["POST"])
@login_required
def checked_item():
    """Update items & completed tables with checked data
    and return new list of List Items asjson object to ajax"""

    checked_items = request.form.getlist("check_item")
    print(checked_items, "checked_items")

    list_id = request.form.get("list_id")

    for checked_item in checked_items:

        checked_item = db.execute("SELECT * FROM items WHERE id = :checked",
                                  checked=checked_item)
        checked_item = checked_item[0]

        # Insert into completed
        db.execute("INSERT INTO completed (name, details, user_id, datetime) VALUES (:name, :details, :user_id, :datetime)",
                   name=checked_item['name'], details=checked_item['details'], user_id=session['user_id'], datetime=get_datetime())
        # Delete from reminders
        db.execute("DELETE FROM items WHERE id = :item_id",
                   item_id=checked_item['id'])

    items = db.execute("SELECT * FROM items WHERE list_id = :list_id",
                       list_id=list_id)

    return (jsonify(items))


@app.route("/checked_goal", methods=["POST"])
@login_required
def checked_goal():
    """Update goals & completed tables with checked data
    and return new list of Goals as json object to ajax"""

    checked_goals = request.form.getlist("check_goal")

    for checked_goal in checked_goals:

        checked_goal = db.execute("SELECT * FROM goals WHERE id = :checked",
                                  checked=checked_goal)
        checked_goal = checked_goal[0]

        # Insert into completed
        db.execute("INSERT INTO completed (name, details, user_id, datetime) VALUES (:name, :details, :user_id, :datetime)",
                   name=checked_goal['name'], details=checked_goal['details'], user_id=session['user_id'], datetime=get_datetime())
        # Delete from reminders
        db.execute("DELETE FROM goals WHERE id = :goal_id",
                   goal_id=checked_goal['id'])

    # Get updated reminders
    goals = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                       user_id=session["user_id"])

    print(checked_goals, "checked_goals")

    return (jsonify(goals))


@app.route("/checked", methods=["POST"])
@login_required
def checked():
    """Update todos & completed tables with checked data
    and return new list of ToDos as json object to ajax"""

    checked_reminders = request.form.getlist("check_reminder")

    for checked_item in checked_reminders:
        print(checked_item, "checked_item")
        checked_reminder = db.execute("SELECT * FROM reminders WHERE id = :checked",
                                      checked=checked_item)
        checked_reminder = checked_reminder[0]

        # Insert into completed
        db.execute("INSERT INTO completed (name, details, user_id, datetime) VALUES (:name, :details, :user_id, :datetime)",
                   name=checked_reminder['name'], details=checked_reminder['details'], user_id=session['user_id'], datetime=get_datetime())
        # Delete from reminders
        db.execute("DELETE FROM reminders WHERE id = :reminder_id",
                   reminder_id=checked_reminder['id'])

    # Get updated reminders
    reminders = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])

    print(checked_reminders, "checked_reminders")

    return (jsonify(reminders))


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete selected ToDo items"""
    checked_reminders = request.form.getlist("check_reminder")
    for checked_reminder in checked_reminders:
        print(checked_reminder, "checked_reminder")
        checked = db.execute("SELECT * FROM reminders WHERE id = :checked_reminder",
                             checked_reminder=checked_reminder)
        checked = checked[0]

        # Delete from reminders
        db.execute("DELETE FROM reminders WHERE id = :reminder_id",
                   reminder_id=checked['id'])

    # Get updated reminders
    reminders = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])
    print(reminders, "reminders")
    return (jsonify(reminders))


@app.route("/delete_goal", methods=["POST"])
@login_required
def delete_goal():
    """Delete selected goal itams"""
    checked_goals = request.form.getlist("check_goal")
    for checked_goal in checked_goals:
        checked = db.execute("SELECT * FROM goals WHERE id = :checked_goal",
                             checked_goal=checked_goal)
        checked = checked[0]

        # Delete from goals
        db.execute("DELETE FROM goals WHERE id = :goal_id",
                   goal_id=checked['id'])

    # Get updated goals
    goals = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                       user_id=session["user_id"])
    print(goals, "goals")
    return (jsonify(goals))


@app.route("/delete_item", methods=["POST"])
@login_required
def delete_item():
    """Delete selected list items"""
    checked_items = request.form.getlist("check_item")
    list_id = request.form.get("list_id")

    for checked_item in checked_items:
        checked = db.execute("SELECT * FROM items WHERE id = :checked_item",
                             checked_item=checked_item)
        checked = checked[0]

        # Delete from items
        db.execute("DELETE FROM items WHERE id = :item_id",
                   item_id=checked['id'])

    # Get updated items
    items = db.execute("SELECT * FROM items WHERE list_id = :list_id",
                       list_id=list_id)
    print(items, "items")
    return (jsonify(items))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# set the secret key.  keep this really secret:
app.secret_key = b'\xe2\x92*\x1b\x96F\xf2\xafh^\xfd\xcf\xde\xb4f\xbd\x0b\xdf\xa1@#\xd4\xb1\x9c'

if __name__ == '__main__':
    app.run()