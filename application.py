import os
import random
import requests

from flask import (
    Flask,
    session,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)
from flask_mail import (
    Mail,
    Message
)
from wtforms import (
    StringField,
    PasswordField,
    BooleanField
)
from wtforms.validators import (
    InputRequired,
    Email,
    Length
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from flask_json import (
    FlaskJSON,
    JsonError,
    json_response,
    as_json
)
from sqlalchemy import create_engine
from flask_session import Session
from flask_wtf import FlaskForm
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure sqlalchemy to connect my DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure email extension
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True cause default is taken from flask_debug env_var
app.config['MAIL_USERNAME'] = 'stanthecompany@gmail.com'
app.config['MAIL_PASSWORD'] = 'stalmax11'
app.config['MAIL_DEFAULT_SENDER'] = 'patryk_stachura@hotmail.com'
app.config['MAIL_MAX_EMAILS'] = 100
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

 #Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

 #Set up database & scope_session for each user
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
##############################################

##########     LOGIN ROUTE          ##########

##############################################
@app.route("/")
def empty():
    if "user" in session:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))
@app.route("/login", methods=['POST', 'GET'])
def login():
    DB_user = Users.query.all()
    if request.method == "POST":
        DB_user = Users.query.all()
        un = request.form["username"]
        pw = request.form["pass"]
        session["user"] = un
        session["password"] = pw
        count = 0
        for user in DB_user:
            if user.username == un and user.password == pw:
                session["user_id"] = user.id
                return redirect(url_for('main')) #MainPage
            else:
                count += 1
                if count < len(DB_user):
                    continue
                else:
                    return  render_template('login_miss.html', title="Something went wrong...",  checkLogs="Username or password incorrected")
                    break
    else:
        return render_template('login.html', title="Login page")
##############################################

##########     LOGGED ROUTE         ##########

##############################################
@app.route("/main/")
@app.route("/main")
def main():
    if "user" in session and "password" in session:
        usr = session["user"]
        return render_template('logged.html', username=usr)
    else:
        return redirect(url_for('login'))
##############################################

##########        LOG OUT           ##########

##############################################
@app.route("/logout")
def logout():
    if "user" in session:
        name = session['user']
        session.pop('user', None)
        session.pop('password', None)
        return render_template('sent.html', message=f"Come back soon... {name} we will miss You.")
    else:
        return redirect(url_for('main'))
##############################################

##########   REGISTRATION ROUTE     ##########

##############################################
@app.route("/registration/", methods=['POST', 'GET'])
@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["pass"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        #password = hashed_password
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        email = request.form["email"]
        phone = request.form["phone"]
        #Select all tables for chacking purpose
        users = Users.query.all()

        for user in users:
            if username == user.username or email == user.email:
                return render_template('registration.html', Register="Username or Email in use.")
                break

        ins = "INSERT INTO users (username, password, first_name, last_name, phone, email) VALUES(:username, :password, :first_name, :last_name, :phone, :email)"

        db.execute(ins, {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email': email})
        db.commit()
        return redirect(url_for('main', usr=username, psw=hashed_password))



    else:
        return render_template('registration.html', title="Registration page", Register="Registration")
##############################################

##########     EMAIL SENDBACK PW    ##########

##############################################
@app.route('/forgot', methods=['POST','GET'])
def email():
    if request.method == 'POST':
        DB_user = Users.query.all()
        email = request.form['email']
        count = 0
        for userEmail in DB_user:
            count += 1
            if email == userEmail.email:
                msg = Message(f'We received a request to return your logs. Your username is {userEmail.username} and your password is {userEmail.password}. Try to keep that in mind', recipients=['stanthecompany@gmail.com', f'{userEmail.email}'])
                mail.send(msg)
                return render_template('sent.html', message="We have recived your logs! Check your email.")
            else:
                if count < len(DB_user):
                    continue
                else:
                    return render_template('sent.html', message=f"Email like {email} doesn\'t exist in our Application")

    else:
        return render_template('email.html')

    return 'Message has been sent'
##############################################

  ##########     SEARCH BOOKS    ##########

##############################################
@app.route('/main', methods=['POST','GET'])
def search():
    if request.method == "POST":
        bookname = request.form["bookname"]
        books = Books.query.filter(Books.title.like(f"%{bookname}%")).all()
        author = Books.query.filter(Books.author.like(f"{bookname}%")).all()
        isbn = Books.query.filter(Books.isbn.like(f"{bookname}")).all()
        value = []
        scores = []
        ### CHECK FOR AUTHORS ###
        if len(author) <= 0:
            del author
        else:
            value = author
        ### CHECK FOR IDs' ###
        if len(isbn) <= 0:
            del isbn
        else:
            value = isbn
        ### CHECK FOR BOOKS ###
        if len(books) <= 0:
            del books
        else:
            value = books
                            ##################################################
                        ####            PROBLEM WITH API's PARAM              ###
                        ####                THAT's WHY CONCAT                 ###
                            ##################################################
        isbns=[]
        isbns_ComaSep = ''
        for each in value:
            isbns.append(each.isbn) ## not working ##
            isbns_ComaSep = isbns_ComaSep + each.isbn + ','

        ############################
        key = "xNVUyD6sffGiUlSclKPAOw"
        secret_key = "QuqGn84nOZOLL6O8Av4LmotDAKkod9m6jdrJ0q3oY2Y"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": f"{key}", "isbns": f"{isbns_ComaSep}"})
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
        respons = res.json()
        #################################

        books = respons['books']
        average_rating_list = []
        review_count_list = []

        for each in books:
            average_rating_list.append(each['average_rating'])
            review_count_list.append(each['reviews_count'])
        ##################################
        ## enrichment our object with  ###
        #### values from outsided API's ##
        ###################################
        counter = 0
        for val in value:
            val.score = average_rating_list[counter]
            val.count = review_count_list[counter]
            counter += 1

        if not value:
            return render_template('logged.html', notFound=notFound)
        else:
            return render_template('logged.html', books=value, score=average_rating_list)
    else:
        return redirect(url_for('main'))
##############################################

    ##########     BOOK PAGE    ##########

##############################################
@app.route('/book/<book_id>/<isbn>/<author>/<title>/<year>', methods=["GET", "POST"])
def bookpage(book_id, isbn, author, title, year):
    usr = session["user"]
    usr_id = session["user_id"]
    ### CHANGE IT TO FUNC IN FUTURE ###
    comments_id = int(book_id)
    comments = Messages.query.filter(Messages.book_id == (f"{comments_id}")).all()
    comments_len = len(comments)
    if comments_len >= 2:
        comments = Messages.query.filter(Messages.book_id == (f"{comments_id}")).offset(comments_len-2).limit(2)

    if request.method == "GET":
        return render_template("page.html", user_id=usr_id, book_id=book_id ,isbn=isbn, author=author, title=title, year=year, user=usr, comments=comments)
    elif request.method == "POST":
        return redirect(url_for('comment' ,user_id=user_id,book_id=book_id, isbn=isbn, author=author, title=title, year=year))
    else:
        return f"ERROR OBJECT NOT FOUND {comments_check}"
##############################################

##########    COMMENTARY SECTION   ##########

#############################################
@app.route('/post/<int:book_id>/<isbn>/<author>/<title>/<year>/<int:user_id>/', methods=["POST"])
def comment(user_id, book_id, isbn, author, title, year):
    name = session["user"]
    comment = request.form["comment"]
    ### CHANGE IT TO FUNC IN FUTURE ###
    comments = Messages.query.filter(and_(Messages.book_id == f"{book_id}",
                                    Messages.user_id == f"{user_id}")).all()
    if len(comments) == 0:
        message = Messages(name=name, message=comment, user_id=user_id, book_id=book_id)
        db.add(message)
        db.commit()
        return redirect(url_for('bookpage', book_id=book_id ,isbn=isbn, author=author, title=title, year=year))
    else:
        return redirect(url_for('bookpage', book_id=book_id ,isbn=isbn, author=author, title=title, year=year))
##############################################

    ##########    API ACCESS    ##########

#############################################
@app.route('/api/<isbn>', methods=["GET"])
def api(isbn):
    key = "xNVUyD6sffGiUlSclKPAOw"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": f"{key}", "isbns": f"{isbn}"})
    if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
    outerAPI = res.json()
    jsonFile = outerAPI['books']
    average_rating = jsonFile[0]['average_rating']
    reviews_count = jsonFile[0]['reviews_count']
    book = Books.query.filter(Books.isbn == f"{isbn}").first()

    if book is None:
        return jsonify({"error": "Invalid book isbn"}), 422
    else:
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": reviews_count,
            "average_score": average_rating
    })
if __name__ == '__main__':
    app.run()
