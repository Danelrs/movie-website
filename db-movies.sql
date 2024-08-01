CREATE DATABASE IF NOT EXISTS db-movies;
USE db-movies;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(45) NOT NULL,
    username VARCHAR(45) NOT NULL,
    password VARCHAR(500) NOT NULL,
);

INSERT INTO users (email, username, password) VALUES ('main@gmail.com', 'admin', 'admin');

CREATE TABLE IF NOT EXISTS cookies (
    id int AUTO_INCREMENT PRIMARY KEY,
    user_id INT foreign key references users(id),
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)