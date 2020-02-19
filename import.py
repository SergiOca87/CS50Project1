import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    "postgres://jsxjwzavvxjudn:574e4c91abeea383f5d4881a0bf5f8cafbc0eecff2063a95c2be4c4c51e2f541@ec2-54-246-90-10.eu-west-1.compute.amazonaws.com:5432/d8p7h9ntpmhmk2")
db = scoped_session(sessionmaker(bind=engine))


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
