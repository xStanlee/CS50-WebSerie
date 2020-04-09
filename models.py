from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book:
    def __init__(self, title, author, year, isbn, review_count, avarge_score):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.review_count = review_count
        self.avarge_score = avarge_score

class Users(db.Model):
    #def __init__(self, username, password, first_name, last_name, phone, email):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)