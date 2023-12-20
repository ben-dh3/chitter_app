from lib.post_repository import *
from datetime import time

def test_get_all_posts(db_connection): 
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    posts = repository.all() 

    assert posts == [
        Post(2, 'message2', time.fromisoformat('13:20:35'), 2, 'username2'),
        Post(1, 'message1', time.fromisoformat('13:20:30'), 1, 'username1'),
    ]