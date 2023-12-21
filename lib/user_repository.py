from lib.user import User
from lib.post import Post
import hashlib
import re

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["id"], row["email"], row["password"], row["username"])
            users.append(item)
        return users
    
    def create(self, user):
        # Hash the password
        binary_password = user.password.encode("utf-8")
        hashed_password = hashlib.sha256(binary_password).hexdigest()

        # Store the email and hashed password in the database
        rows = self._connection.execute(
            'INSERT INTO users (email, password, username) VALUES (%s, %s, %s) RETURNING id',
            [user.email, hashed_password, user.username])
        user.id = rows[0]['id']

    def check_password(self, email, password):
        # Hash the password attempt
        binary_password_attempt = password.encode("utf-8")
        hashed_password_attempt = hashlib.sha256(binary_password_attempt).hexdigest()
        # Check whether there is a user in the database with the given email
        # and a matching password hash, using a SELECT statement.
        rows = self._connection.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s',
            [email, hashed_password_attempt])

        # If that SELECT finds any rows, the password is correct.
        return len(rows) > 0
    
    def find_by_email(self, email):
        rows = self._connection.execute(
            "SELECT users.id AS user_id, users.email AS user_email, users.password AS user_password, users.username AS username " \
            "FROM users " \
            "WHERE users.email = %s", [email])
        
        if len(rows) < 1:
            return None
        return User(rows[0]["user_id"], rows[0]["user_email"], rows[0]["user_password"], rows[0]["username"])

    def validity_checker(self, email, password):
        if email is None or password is None:
            return False
        if re.match(r"^\S+@\S+\.\S+$", email, re.I) and re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
            return True
        else:
            return False
        
    def check_username_unique(self, username):
        rows = self._connection.execute(
            "SELECT * " \
            "FROM users " \
            "WHERE users.username = %s", [username])
        
        if len(rows) > 0:
            return False
        return True

