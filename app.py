import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
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
@app.route("/index")
def index():
    return render_template ("index.html")


@app.route("/bagels")
def bagels():
    breakfast = mongo.db.product.find({"category_name":"breakfast"})
    bagelwiches = mongo.db.product.find({"category_name":"bagelwiches"})
    openfaced = mongo.db.product.find({"category_name":"open-faced"})
    pizzabagels = mongo.db.product.find({"category_name":"pizza-bagels"})
    wrap = mongo.db.product.find({"category_name":"wraps"})
    other = mongo.db.product.find({"category_name":"lite-bites"})

    return render_template("bagels.html", breakfast=breakfast, bagelwiches=bagelwiches, 
    openfaced=openfaced, pizzabagels=pizzabagels, wrap=wrap, other=other)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        new_user = {
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password"))
        }

        mongo.db.user.insert_one(new_user)
        session["user"] = request.form.get("username").lower()
        
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
