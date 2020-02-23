import os

from flask import Flask, render_template, request, session
from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

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
# I should identify how to use Databases and Sessions together, is that necessary?
# Or does a DB substitutes Sessions alltogether?
@app.route("/", methods=["GET", "POST"])
def index():

    # Check if there is anything in the books Session first
    if session.get('books') is None:
        # Initiate an empty list of books for this session
        session["books"] = []

    # If the user is logged in, they would see a form
    # Which they can POST, and we can use Session to store the book they submit
    if request.method == "POST":
        book = request.form.get("book")
        session["books"].append(book)
        loggedIn=True
        return render_template('index.html', loggedIn=loggedIn, name=name, books=session["books"])

    return render_template('index.html', loggedIn=loggedIn, name=name)


@app.route("/login")
def login():
    return render_template('login.html')

# This Route accepts get and Post methods,
# Get so we can see the page. Post so we can post the register form
@app.route("/register", methods=["GET", "POST"])
def register():
    name = request.form.get("name")

    if request.method == "GET":
        return render_template('register.html')
    else:
        loggedIn = True 
        return render_template('index.html', name=name, loggedIn=loggedIn)

# Example of a dynamic route
# @app.route("/<string:name>")
# def hello(name):
#     return "Hello, {}!".format(name)

# Route with a variable
@app.route('/book')
def book():
    title = "Book Title Test"
    return render_template('book.html', title=title)


@app.route('/user')
def user():
    userName = "Joe"
    userBooks = ['Book 1', 'Book 2', 'Book 3']
    return render_template('user.html', userBooks=userBooks, userName=userName)