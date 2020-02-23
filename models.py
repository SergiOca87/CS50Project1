# Where we define classes, classes interact directly with our db
#For any table inside of the database, there is one class defined inside models.py.
# Books
import os

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

#Flask SQLAlchemy not allowed for this project
# class Book(db.Model):
#     __tablename__ = "books"
#     id = db.Column(db.Integer, primary_key=True)
#     isbn = db.Column(db.String, nullable=False)
#     title = db.Column(db.String, nullable=False)
#     author = db.Column(db.Integer, nullable=False)
#     pub_year = db.Column(pub_year.Integer, nullable=False)

# class User(db.Model):
#     __tablename__= "users"  
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     password = db.Column(db.String, nullable=False)


class Book:
    def __init__(self, isbn, title, author, pub_year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.pub_year = pub_year

class User:
    def __init__(self, username, passwordr):
        self.username = username
        self.password = password