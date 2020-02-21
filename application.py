import os
# import csv

from flask import Flask, render_template, session, request
from models import *
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
 app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

    def main():
        # Create tables based on each table definition in `models`
        db.create_all()

    if __name__ == "__main__":
        # Allows for command line interaction with Flask application
        with app.app_context():
            main()

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('index.html')
