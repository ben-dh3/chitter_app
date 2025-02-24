from lib.post import Post

class PostRepository:

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT users.id AS user_id, users.username AS username, posts.id AS post_id, posts.message AS message, posts.time AS time, posts.user_id AS post_user_id ' \
                                        'FROM users JOIN posts ON users.id = posts.user_id')
        posts = []
        for row in rows:
            item = Post(row["post_id"], row["message"], row["time"], row["user_id"], row["username"] )
            posts.append(item)
        posts.reverse()
        return posts
    
    def create(self, post):
        rows = self._connection.execute(
            'INSERT INTO posts (message, time, user_id, username) VALUES (%s, %s, %s, %s) RETURNING id', 
            [post.message, post.time, post.user_id, post.username]
        )
        post_id = rows[0]['id']
        return None
    
    # list of posts by specific user
    def find_by_user(self, user_id):
        rows = self._connection.execute(
            "SELECT users.id AS user_id, users.email, posts.id AS post_id, posts.message AS message, posts.time AS time, posts.user_id AS user_id, posts.username AS post_username " \
            "FROM users JOIN posts ON users.id = posts.user_id " \
            "WHERE users.id = %s", [user_id])
        posts = []
        for row in rows:
            post = Post(row["post_id"], row["message"], row["time"], row["user_id"], row["post_username"])
            posts.append(post)
        posts.reverse()
        return posts

    # returns username of the creator of a post
    def find_username_with_userid(self, user_id):
        rows = self._connection.execute(
            "SELECT users.id, users.username AS username " \
            "FROM users " \
            "WHERE users.id = %s", [user_id])
        username = rows[0]["username"]
        return username
    
    # returns the email attached to a username in a post
    def find_email_by_username(self, username):
        rows = self._connection.execute(
            "SELECT users.email AS user_email, users.username AS username " \
            "FROM users " \
            "WHERE users.username = %s", [username])
        
        if len(rows) > 0:
            email = rows[0]["user_email"]
            return email
        return None

    def delete(self, post_id, user_id):
        """Delete a post if it belongs to the user"""
        rows = self._connection.execute(
            'DELETE FROM posts WHERE id = %s AND user_id = %s RETURNING id',
            [post_id, user_id]
        )
        return len(rows) > 0

    def update(self, post_id, user_id, new_message):
        """Update a post's message if it belongs to the user"""
        rows = self._connection.execute(
            'UPDATE posts SET message = %s WHERE id = %s AND user_id = %s RETURNING id',
            [new_message, post_id, user_id]
        )
        return len(rows) > 0

    def find_by_id(self, post_id):
        """Find a post by its ID"""
        rows = self._connection.execute(
            'SELECT posts.id AS post_id, posts.message, posts.time, posts.user_id, posts.username ' \
            'FROM posts WHERE posts.id = %s',
            [post_id]
        )
        if len(rows) == 0:
            return None
        row = rows[0]
        return Post(row["post_id"], row["message"], row["time"], row["user_id"], row["username"])