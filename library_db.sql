-- Create the database first in PostgreSQL
CREATE DATABASE library_db;

-- Books table
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(50),
    quantity INT
);

-- Members table
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- Borrow table
CREATE TABLE borrow (
    borrow_id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(book_id),
    member_id INT REFERENCES members(member_id),
    borrow_date DATE,
    return_date DATE,
    status VARCHAR(20)
);

--insert sample books records
INSERT INTO books (title, author, genre, quantity) VALUES
('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 5),
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 3),
('1984', 'George Orwell', 'Dystopian', 4),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 2),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 6);

--insert sample members records
INSERT INTO members (name, phone, email) VALUES
('Alice Johnson', '1234567890', 'alice@example.com'),
('Bob Smith', '9876543210', 'bob@example.com'),
('Charlie Brown', '5555555555', 'charlie@example.com'),
('Daisy Miller', '4444444444', 'daisy@example.com'),
('Ethan Hunt', '3333333333', 'ethan@example.com');
