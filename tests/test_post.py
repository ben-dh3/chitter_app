from lib.post import Post

def test_post_constructs():
    post = Post(1, "Test Post", "13:30:30", 1)
    assert post.id == 1
    assert post.message == "Test Post"
    assert post.time == "13:30:30"
    assert post.user_id == 1

def test_post_format_nicely():
    post = Post(1, "Test Post", "13:30:30", 1)
    assert str(post) == "Post(1, Test Post, 13:30:30, 1)"

def test_posts_are_equal():
    post1 = Post(1, "Test Post", "13:30:30", 1)
    post2 = Post(1, "Test Post", "13:30:30", 1)
    assert post1 == post2