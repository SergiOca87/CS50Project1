import csv
import os


from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:  # loop gives each column a name
        db.execute("INSERT INTO books (isbn, title, author, pub_year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "pub_year": year})  # substitute values from CSV line into SQL command, as per this dict
        print(f"Added book {title} to the database")
    db.commit()  # transactions are assumed, so close the transaction finished


if __name__ == "__main__":
    main()
