import os
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

    per_page = 9

    page = request.args.get(get_page_parameter(), type=int, default=1)

    games = list(mongo.db.games.find())

    pagination = Pagination(page=page, per_page=per_page, total=len(games))

    return render_template("index.html", 
                            games=display_games(games,page,per_page),
                            pagination=pagination,
                            username=get_user())


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
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
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
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
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
                "password": generate_password_hash(request.form.get("password"))
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

    reviews = list(mongo.db.reviews.find({"created_by": username}))

    games = list(mongo.db.games.find({"created_by": username}))

    if session["user"]:
        return render_template("profile.html", 
                                username=username,
                                reviews=reviews,
                                games=games)

    return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
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
        return redirect(url_for("profile", username=get_user()))

    games = mongo.db.games.find().sort("name", 1)

    return render_template("add_review.html", 
                            games=games,
                            username=get_user())


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
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
        return redirect(url_for("profile", username=get_user()))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    return render_template("edit_review.html", 
                            username=get_user(), 
                            review=review)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfully Deleted")
    return redirect(url_for("profile", username=get_user()))


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        submit = {
            
        }
        mongo.db.games.insert_one(submit)
        flash("Game Successfully Added")
        return redirect(url_for("profile", username=get_user()))

    return render_template("add_game.html", 
                            username=get_user())


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    if request.method == "POST":
        img_link = request.form.get("img_link")
        
        if len(img_link) < 1:
            img_link = game["img_link"]

        submit = {
            "name": game['name'],
            "description": request.form.get("description"),
            "category_name": request.form.get("category_name"),
            "img_link": img_link,
            "created_date": game['created_date'],
            "updated_date": datetime.today().strftime('%d-%m-%Y'),
            "created_by": session["user"]
        }
        mongo.db.games.update({"_id": ObjectId(game_id)}, submit)
        flash("Game Successfully Updated")
        return redirect(url_for("profile", username=get_user()))

    categories = mongo.db.categories.find().sort("category_name", 1)

    return render_template("edit_game.html", 
                            username=get_user(), 
                            game=game,
                            categories=categories)


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    flash("Game Successfully Deleted")
    return redirect(url_for("profile", username=get_user()))


@app.route("/display_game/<game_id>", methods=["GET"])
def display_game(game_id):

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    reviews = list(mongo.db.reviews.find({"game_name":game["name"]}))

    return render_template("display_game.html", 
                            username=get_user(), 
                            game=game,
                            reviews=reviews)


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
    try:
        user = session["user"]
        return user
    except:
        user = ''
        return user


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            