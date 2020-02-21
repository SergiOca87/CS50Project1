-- Books table

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    pub_year INTEGER NOT NULL
);

-- User Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    pass VARCHAR NOT NULL
)

-- Review Table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    stars INTEGER NOT NULL,
    review VARCHAR NOT NULL
)