from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey
)

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
    ### RELATION ONE TO MANY ###
    parent_user = relationship("Messages", back_populates="user")
    ############################
    def last_index(self):
        return len(self)-1

    def __repr__(self):
        return '<Users %r>' % self.username

class Books(db.Model):

    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
     ### RELATION ONE TO MANY ###
    parent_book = relationship("Messages", back_populates="book")
    ############################
    def __repr__(self):
        return '<Books %r>' % self.title

class Messages(db.Model):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', back_populates="parent_user")
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book = db.relationship('Books', back_populates="parent_book")
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Messages %r>' % self.message