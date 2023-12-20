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
    time time,
    user_id INTEGER,
    username VARCHAR(255)
);


INSERT INTO users (email, password, username) VALUES ('email1', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'username1');
INSERT INTO users (email, password, username) VALUES ('email2', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', 'username2');
INSERT INTO users (email, password, username) VALUES ('email3', '5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764', 'username3');

INSERT INTO posts (message, time, user_id, username) VALUES ('message1', '13:20:30', 1, 'username1');
INSERT INTO posts (message, time, user_id, username) VALUES ('message2', '13:20:35', 2, 'username2');