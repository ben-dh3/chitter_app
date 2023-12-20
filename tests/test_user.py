from lib.user import User

def test_user_constructs():
    user = User(1, "email", "password", "username")
    assert user.id == 1
    assert user.email == "email"
    assert user.password == "password"
    assert user.username == "username"

def test_user_format_nicely():
    user = User(1, "email", "password", "username")
    assert str(user) == "User(1, email, password, username)"

def test_posts_are_equal():
    user1 = User(1, "email", "password", "username")
    user2 = User(1, "email", "password", "username")
    assert user1 == user2