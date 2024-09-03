DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password CHAR(64),
    username VARCHAR(255)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    message VARCHAR(255),
    time VARCHAR(255),
    user_id INTEGER,
    username VARCHAR(255)
);