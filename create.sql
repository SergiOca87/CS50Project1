-- Books table
-- The book table references the user table as I want to associate books to users
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL,
    user_id INTEGER REFERENCES users
);

-- User Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    pass VARCHAR NOT NULL
);

-- Review Table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    stars INTEGER NOT NULL,
    review VARCHAR,
    book_id INTEGER REFERENCES books
);