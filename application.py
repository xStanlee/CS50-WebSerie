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

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Request for jsonFile
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "cIAWnULXTSoqvTIKqOMdTQ", "isbns": "9781632168146"})
resJson = res.json()

@app.route("/")
def empty():
    usersName = Users.query.first()
    return(f"WORK ? HASSWORD - {usersName.password} LOGINS - {usersName.username} PHONE {usersName.phone}")#redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["pass"]
    else:
        return render_template('login.html', title="Login page")

@app.route("/test/<usr>/<psw>")
def test(usr, psw):
    return f"USER : {usr}, PASSWORD: {psw}"

@app.route("/registration/")
def registration():
    return render_template('registration.html', title="Registration page")