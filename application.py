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



@app.route("/", methods=["GET", "POST"])
def index():

    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user") is None:
        session["user"] = []
    # Get user and pass, look it up in the db:
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE username = :username AND pass = :pass", {"username": username, "pass": password}).fetchone()

        if user is None:
            return render_template("error.html", message="Sorry, the username or pass does not match")

        session["user"] = []
        session["user"].append(username)
        session["user"].append(user.id)

        return render_template('user.html', username=session['user'][0], user_id=session['user'][1])

    return render_template('login.html')

# This Route accepts get and Post methods,
# Get so we can see the page. Post so we can post the register form
@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "GET":
        return render_template('register.html')
    else:
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


# Single Book route
# maybe use isbn as the url?
@app.route('/books/<title>')
def books(title):

    # First thing is to check that the book exists
    book = db.execute("SELECT * FROM books WHERE title = :title", {"title": title}).fetchone()
    bookId = book['id']
    isbn = book['isbn']  

    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": bookId}).fetchall()
    users = db.execute("SELECT * FROM users").fetchall()
    reviewsBy = []

    # Loop through each review to find out wich user left each review
    for review in reviews:
        # The id of the user used as an index, minus one as the ids are not 0 zero based
        user=review['user_id'] - 1
        # From the users Array, push into the reviewsBy the username, using their ids as the index (from the previous step)
        reviewsBy.append(users[user][1])
     

    if book is None:
        return render_template("error.html", message="Sorry, this book was not found in our database")

    # Make a request to the Goodreads API using the book isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADSKEY"), "isbns": isbn})

    # Parse the API result to JSON
    data = res.json()

    # Get the average rating from Goodreads
    avg_rating = data['books'][0]['average_rating']

    return render_template("book.html", book=book, avg_rating=avg_rating, reviews=reviews, reviewsBy=reviewsBy)

# Route designed to leave the reviews
@app.route('/book', methods=["POST"]) 
def book():

    # Get form information.
    stars = int(request.form.get("stars"))
    review = request.form.get("review")
    book_id = request.form.get("book_id")
   

    # Retake Here :
    # Users should not be able to submit multiple reviews for the same book.
    # Use the new user_id column in the reviews table to associate reviews with users
    # We can also show a by: {username} with that

    # Make surethe book exists.
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return render_template("error.html", message="No such book with that id was found in our database.")
    db.execute("INSERT INTO reviews (stars, review, book_id, user_id) VALUES (:stars, :review, :book_id, :user_id)",
            {"stars": stars, "review": review, "book_id": book_id, "user_id": session['user'][1]})
    db.commit()
    return render_template("reviewsuccess.html")




@app.route('/user', methods=["GET", "POST"])
def user():

    if request.method == "POST":
        searchValue = "%" + request.form.get("booksearch") + "%"

        if db.execute("SELECT * FROM books WHERE isbn LIKE :searchValue OR title LIKE :searchValue OR author LIKE :searchValue OR year LIKE :searchValue", {"searchValue": searchValue}).rowcount == 0:
            return render_template("error.html", message="Sorry, the book you were looking for was not found.")
        books = db.execute("SELECT * FROM books WHERE title LIKE :searchValue OR isbn LIKE :searchValue OR author LIKE :searchValue LIMIT 10",
                           {"searchValue": searchValue}).fetchall()

        return render_template('books.html', books=books, username=session['user'])

        
