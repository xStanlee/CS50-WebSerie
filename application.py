import os
import requests

from flask import session, render_template, request, redirect, url_for
from flask_session import Session
from flask_mail import Mail, Message
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

# Configure email extension
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True
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

#//////////////////////////
#/// FOR LATER USAGE

# Request for jsonFile
#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "cIAWnULXTSoqvTIKqOMdTQ", "isbns": "9781632168146"})
#resJson = res.json()

@app.route("/")
def empty():
    return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    DB_user = Users.query.all()
    if request.method == "POST":
        DB_user = Users.query.all()
        un = request.form["username"]
        pw = request.form["pass"]
        count = 0
        for user in DB_user:
            if user.username == un and user.password == pw:
                return redirect(url_for('test', usr=un, psw=pw)) #MainPage
            else:
                count += 1
                if count < len(DB_user):
                    continue
                else:
                    return  render_template('login_miss.html', title="Something went wrong...",  checkLogs="Username or password incorrected")
                    break



    else:
        return render_template('login.html', title="Login page")

@app.route("/test/<usr>/<psw>")
def test(usr, psw):
    return f"USER : {usr}, PASSWORD: {psw}"

@app.route("/registration/", methods=['POST', 'GET'])
@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["pass"]
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        email = request.form["email"]
        phone = request.form["phone"]

#//////////////////////////
#/////////
        #Select all tables for chacking purpose
        users = Users.query.all()

        for user in users:
            if username == user.username or email == user.email:
                return render_template('registration.html', Register="Username or Email in use.")
                break

        ins = "INSERT INTO users (username, password, first_name, last_name, phone, email) VALUES(:username, :password, :first_name, :last_name, :phone, :email)"

        db.execute(ins, {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email': email})
        db.commit()
        return redirect(url_for('test', usr=username, psw=password))



    else:
        return render_template('registration.html', title="Registration page", Register="Registration")

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
if __name__ == '__main__':
    app.run()

@app.route('/send')
def send():
    msg = Message('Test message: Koronawirus_precz2020_july', recipients=['kogopo4822@govdep5012.com', 'stachura.patryk@yahoo.com'])
    mail.send(msg)

    return 'Message has been sent'
if __name__ == '__main__':
    app.run()