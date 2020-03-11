import os
import requests

from flask import Flask, render_template, request, session
from flask_session import Session

# sqlalchemy is used to use sql commands in flask apps, to communicate with dbs
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# The engine Object manages connections to the DB, ittranslates Python to SQl for us and gets results back from the DB
# It uses a env variable for the DB URL
engine = create_engine(os.getenv("DATABASE_URL"))

# Scoped sessions are used to handle multiple connections from different users
# The db variable is what will allow us to run SQL commands
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)

# Configure session to use filesystem
# Sessions, a way to store permanent data
# With Sessions, we can store this data serverside, so upon server restart we keep that data
# Session is a variable that is available only to the specific "session", like a browser session or user
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


# Tell Flask what SQLAlchemy database to use.
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")


# Link the Flask app with the database (no Flask app is actually being run yet).
# db.init_app(app)


# def main():
#     # Create tables based on each table definition in `models`
#     db.create_all()


# if __name__ == "__main__":
#     # Allows for command line interaction with Flask application
#     with app.app_context():
#         main()

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


# User must be able to register. /register route with a form
# This form should create a user, maybe using the model, a table should exist for users


# User should be able to log in, in the /login route
# Should search the users table for matches
# In terms of how to “log a user in,” recall that you can store information inside of the session, which can store different values for different users.
# In particular, if each user has an id, then you could store that id in the session (e.g., in session["user_id"]) to keep track of which user is currently logged in.


# Once a user has logged in, they should be taken to a page where they can search for a book.
# Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book.
# After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches.
# If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
# Should I retrieve and display all of the books assdociated with a user?
# SELECT title, name FROM books JOIN users ON users.user_id = users.id;


# Book Page: When users click on a book from the results of the search page, they should be taken to a book page,
# details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.


# Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book.
# Users should not be able to submit multiple


# The user must be able to search for a book and retrieve it
# Use a search and a form for this with a post method


# Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.


# # List all Books
# books = db.execute("SELECT id, title FROM books").fetchall()
# for book in books:
#     print(f"Book {book.id}: {book.title}")
loggedIn = False
name = ''


# State of the App:
# Sessions do work but loggedIn and Name are global variables to test things out
# I should identify how to use Databases and Sessions together.


# airline1 has info on how to query a relationship, could use it to relate books with users

# I guess sessions could be used to keep track of a user if they are logged in, in a current session

# In line 201, book is undefined, we are close

@app.route("/", methods=["GET", "POST"])
def index():

    # Check if there is anything in the books Session first
    # if session.get('books') is None:
    # Initiate an empty list of books for this session
    # session["books"] = []

    # If the user is logged in, they would see a form
    # Which they can POST, and we can use Session to store the book they submit
    # if request.method == "POST":
    #     searchValue = request.form.get("book")

    #     if db.execute("SELECT * FROM books WHERE title = :title", {"title" : searchValue}).rowcount == 0:
    #         return render_template("error.html", message="Sorry, the book you were looking for was not found.")
    #     books = db.execute("SELECT * FROM books WHERE title = :title", {"title" : searchValue}).fetchall()
    #     return render_template('books.html', books=books)
    # session["books"].append(book)
    # loggedIn=True

    return render_template('index.html', loggedIn=loggedIn, name=name)
    # try / except for handling empty imputs?


@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user") is None:
        session["user"] = []
    # Get user and pass, look it up in the db:
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        session["user"] = []
        session["user"].append(username)
        # SELECT * FROM users;
        # WHERE (username = username)
        # AND (pass = pass);
        if db.execute("SELECT * FROM users WHERE username = :username AND pass = :pass", {"username": username, "pass": password}).rowcount == 0:
            return render_template("error.html", message="Sorry, the username or pass does not match")
        return render_template('user.html', username=session['user'], loggedIn=True)

    return render_template('login.html')
    # Retrieve a list of the books from the User:
    # books = db.execute("SELECT isbn, title, author, pub_year, user FROM books JOIN users ON users.book_id = books.id").fetchall()
    # for book in books:
    #     print(f"{book.title}")


# This Route accepts get and Post methods,
# Get so we can see the page. Post so we can post the register form
@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "GET":
        return render_template('register.html')
    else:
        loggedIn = True

        # # Insert user into the DB?
        # INSERT INTO users (name, pass) VALUES (name, pass);

        # # retrieve users from table
        # SELECT * FROM users;

        if db.execute("SELECT * FROM users WHERE username = :username AND pass = :pass", {"username": username, "pass": password}).rowcount == 0:
            db.execute("INSERT INTO users (username, pass) VALUES (:username, :pass)", {
                       "username": username, "pass": password})
            db.commit()
            return render_template('success.html')
        return render_template("error.html", message="We already have an account with that name and pass")


@app.route('/logout', methods=['GET'])
def logout():
    if session.get("user"):
        session["user"] = []
    return render_template("index.html")
# Example of a dynamic route
# @app.route("/<string:name>")
# def hello(name):
#     return "Hello, {}!".format(name)

# Single Book route
# maybe use isbn as the url?
@app.route('/book/<string:title>')
def book(title):

    # First thing is to check that the book exists
    book = db.execute("SELECT * FROM books WHERE title = :title",
                      {"title": title}).fetchone()
    if book is None:
        return render_template("error.html", message="Sorry, this book was not found in our database")

    # if the book is found, render the book template passing in the book details
    return render_template("book.html", book=book)


@app.route('/user', methods=["GET", "POST"])
def user():

    if request.method == "POST":
        searchValue = "%" + request.form.get("booksearch") + "%"

        if db.execute("SELECT * FROM books WHERE isbn LIKE :searchValue OR title LIKE :searchValue OR author LIKE :searchValue OR year LIKE :searchValue", {"searchValue": searchValue}).rowcount == 0:
            return render_template("error.html", message="Sorry, the book you were looking for was not found.")
        books = db.execute("SELECT * FROM books WHERE title LIKE :searchValue OR isbn LIKE :searchValue OR author LIKE :searchValue LIMIT 10",
                           {"searchValue": searchValue}).fetchall()

        
        # Retake here:
        # Just getting the last ISBN, data only prints the last result
        # This works to store the different isbns:
        isbns = [];
        length = len(books) 
        for i in range(length): 
            isbns.append(books[i][1]) 

        print('isbns', isbns)
        # Goodreads APP
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": os.getenv("GOODREADSKEY"), "isbns": isbns})
        data = res.json()

        print('data', data)
        avg_rating = data['books'][0]['average_rating']
        return render_template('books.html', books=books, username=session['user'], avg_rating=avg_rating)

        
