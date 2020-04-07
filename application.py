import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure sqlalchemy to connect my DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

 #Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

 #Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
# Request for jsonFile
#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "cIAWnULXTSoqvTIKqOMdTQ", "isbns": "9781632168146"})
#resJson = res.json()

@app.route("/")
def empty():
    usersName = Users.query.all()
    return f"Zwracacz {usersName[1].password}"

@app.route("/login", methods=['POST', 'GET'])
def login():
    usersName = Users.query.all()
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["pass"]
        usersName = Users.query.all()
        for single in usersName:
            if single.password == password and single.username == user:
                return redirect(url_for('test', usr=user, psw=password))
                break
            else:
                return render_template('login_miss.html', title="Something went wrong...",  checkLogs="Username or password incorrected")
        #return redirect(url_for('test', usr=user, psw=password))
    else:
        return render_template('login.html', title="Login page")

@app.route("/test/<usr>/<psw>")
def test(usr, psw):
    return f"USER : {usr}, PASSWORD: {psw}"

@app.route("/registration/", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":

        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        username = request.form["username"]
        password = request.form["pass"]
        email = request.form["email"]
        phone = request.form["phone"]
        # Select all tables for chacking purpose
        users = Users.query.all()

        for user in users:
            if username == user.username or email == user.email:
                return "User with that username exists or email is in use"
                break
            else:
                newUser = Users(username=username,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email)
                session = Session ()
                session.add(newUser)
                return redirect(url_for('test', usr=newUser.username, psw=newUser.password))
            session.commit()


    else:
        return render_template('registration.html', title="Registration page")