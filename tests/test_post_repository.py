from lib.post_repository import *
from datetime import time, datetime

def test_get_all_posts(db_connection): 
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    posts = repository.all() 

    assert posts == [
        Post(2, 'message2', time.fromisoformat('13:20:35'), 2, 'username2'),
        Post(1, 'message1', time.fromisoformat('13:20:30'), 1, 'username1'),
    ]

def test_create_post(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    current_time = time.fromisoformat('18:22:38')
    post = Post(None, 'message3', current_time, 2, 'username2')
    repository.create(post)

    posts = repository.all() 
    assert posts == [
        Post(3, 'message3', time.fromisoformat('18:22:38'), 2, 'username2'),
        Post(2, 'message2', time.fromisoformat('13:20:35'), 2, 'username2'),
        Post(1, 'message1', time.fromisoformat('13:20:30'), 1, 'username1'),
    ]

def test_find_by_user(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    posts = repository.find_by_user(1)
    assert posts == [
        Post(1, 'message1', time.fromisoformat('13:20:30'), 1, 'username1')
    ]

def test_find_username_with_userid(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    username = repository.find_username_with_userid(1)

    assert username == 'username1'

def test_find_email_by_username(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = PostRepository(db_connection)
    email = repository.find_email_by_username('username1')

    assert email == 'email1'



