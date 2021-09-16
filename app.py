import os
import base64
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    """
    This method loads the games in the DB into a list
    for pagination and display on he index page
    """
    per_page = 9

    page = request.args.get(get_page_parameter(), type=int, default=1)

    games = list(mongo.db.games.find())

    pagination = Pagination(page=page, per_page=per_page, total=len(games))

    return render_template("index.html",
                           games=display_games(games, page, per_page),
                           pagination=pagination,
                           username=get_user(),
                           acc_type=get_acc_type())


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Used Code from the Flask task project
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session["acc_type"] = existing_user["type"]
                return redirect(url_for(
                    "profile", username=get_user()))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Remove session to log user out
    """
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    session.pop("acc_type")
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Used Code from the Flask task project
    Added custom code for password validation
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        # Custom code
        if request.form.get("password") == request.form.get("conpassword"):
            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "type" : "user"
            }
            mongo.db.users.insert_one(register)

            # put the new user into 'session' cookie
            session["user"] = request.form.get("username").lower()
            return redirect(url_for("profile", username=session["user"]))
        else:
            flash("Passwords do not match")
            return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Used Code from the Flask task project
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    users = list(mongo.db.users.find())

    reviews = list(mongo.db.reviews.find({"created_by": username}))

    games = list(mongo.db.games.find({"created_by": username}))

    if session["user"] and get_acc_type() == "user":
        return render_template("profile.html",
                               username=username,
                               reviews=reviews,
                               games=games)
    elif session["user"] and get_acc_type() == "admin":
        return render_template("admin.html",
                               username=username,
                               reviews=reviews,
                               games=games,
                               users=users)
    else:
        return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """
    Add a review to a game
    """
    if request.method == "POST":
        submit = {
            "game_name": request.form.get("game_name"),
            "review_description": request.form.get("review_description"),
            "created_date": datetime.today().strftime('%d-%m-%Y'),
            "updated_date": datetime.today().strftime('%d-%m-%Y'),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(submit)
        flash("Review Successfully Added")
        if get_acc_type() == "admin":
            return redirect(url_for("admin", username=get_user()))
        else:
            return redirect(url_for("profile", username=get_user()))

    games = mongo.db.games.find().sort("name", 1)

    return render_template("add_review.html",
                           games=games,
                           username=get_user(),
                           acc_type=get_acc_type())


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """
    Edit selected review
    """
    if request.method == "POST":
        review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        submit = {
            "game_name": review['game_name'],
            "review_description": request.form.get("review_description"),
            "created_date": review['created_date'],
            "updated_date": datetime.today().strftime('%d-%m-%Y'),
            "created_by": session["user"]
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")
        if get_acc_type() == "admin":
            return redirect(url_for("admin", username=get_user()))
        else:
            return redirect(url_for("profile", username=get_user()))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    return render_template("edit_review.html",
                           username=get_user(),
                           review=review,
                           acc_type=get_acc_type())


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    """
    Delete selected review
    """
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfully Deleted")
    if get_acc_type() == "admin":
        return redirect(url_for("admin", 
                        username=get_user(),
                        acc_type=get_acc_type()))
    else:
        return redirect(url_for("profile", 
                        username=get_user(),
                        acc_type=get_acc_type()))


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    """
    Add new game to the DB
    """
    if request.method == "POST":
        game = mongo.db.games.find_one({"name": request.form.get("name")})
        file = request.files['img_link']
        rv = base64.b64encode(file.read())
        rv = rv.decode('ascii')
        if game is not None:
            flash("Game Already Exists")
        else:
            submit = {
                "name": request.form.get("name"),
                "description": request.form.get("description"),
                "category_name": request.form.get("category_name"),
                "img_link": rv,
                "created_date": datetime.today().strftime('%d-%m-%Y'),
                "updated_date": datetime.today().strftime('%d-%m-%Y'),
                "created_by": session["user"]
            }

            mongo.db.games.insert_one(submit)
            flash("Game Successfully Added")
            if get_acc_type() == "admin":
                return redirect(url_for("admin", 
                                username=get_user(),
                                acc_type=get_acc_type()))
            else:
                return redirect(url_for("profile", 
                            username=get_user(),
                            acc_type=get_acc_type()))

    categories = mongo.db.categories.find().sort("category_name", 1)

    return render_template("add_game.html",
                           username=get_user(),
                           categories=categories,
                           acc_type=get_acc_type())


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    """
    Edit selected game
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    if request.method == "POST":
        file = request.files['img_link']
        rv = base64.b64encode(file.read())
        rv = rv.decode('ascii')
        submit = {
            "name": game['name'],
            "description": request.form.get("description"),
            "category_name": request.form.get("category_name"),
            "img_link": rv,
            "created_date": game['created_date'],
            "updated_date": datetime.today().strftime('%d-%m-%Y'),
            "created_by": session["user"]
        }
        mongo.db.games.update({"_id": ObjectId(game_id)}, submit)
        flash("Game Successfully Updated")
        if get_acc_type() == "admin":
            return redirect(url_for("admin", 
                            username=get_user(),
                            acc_type=get_acc_type()))
        else:
            return redirect(url_for("profile", 
                            username=get_user(),
                            acc_type=get_acc_type()))

    categories = mongo.db.categories.find().sort("category_name", 1)

    return render_template("edit_game.html",
                           username=get_user(),
                           game=game,
                           categories=categories,
                           acc_type=get_acc_type())


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    """
    Delete selected game
    """
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    flash("Game Successfully Deleted")
    if get_acc_type() == "admin":
        return redirect(url_for("admin", 
                        username=get_user(),
                        acc_type=get_acc_type()))
    else:
        return redirect(url_for("profile", 
                        username=get_user(),
                        acc_type=get_acc_type()))


@app.route("/display_game/<game_id>", methods=["GET"])
def display_game(game_id):
    """
    This method returns the selected game and
    reviews.
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    reviews = list(mongo.db.reviews.find({"game_name": game["name"]}))

    return render_template("display_game.html",
                           username=get_user(),
                           game=game,
                           reviews=reviews,
                           acc_type=get_acc_type())


@app.route("/delete_user/<user_id>", methods=["GET"])
def delete_user(user_id):
    """
    This method deletes the selected user, games and
    reviews.
    """
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    flash("User has been removed")
    return redirect(url_for("login"))


def display_games(game_list, curr_page, per_page):
    """
    Method to handle Pagination of games.
    Give a list of games, the current page the user is on and
    the number of games to display it returns a list of games
    """

    next_index = 9

    games_to_display = []

    if curr_page > 1:
        offset = (curr_page - 1) * per_page
        if (offset + next_index) > len(game_list):
            games_to_display = game_list[offset:]
        else:
            games_to_display = game_list[offset:next_index]
    else:
        offset = 0
        games_to_display = game_list[offset:next_index]

    return games_to_display


def get_user():
    """
    Method returns the user in the Session
    """
    try:
        user = session["user"]
        return user
    except:
        user = ''
        return user


def get_acc_type():
    """
    Method returns the account type in the Session
    """
    try:
        acc_type = session["acc_type"]
        return acc_type
    except:
        acc_type = ''
        return acc_type


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
