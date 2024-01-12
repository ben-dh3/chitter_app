from lib.user_repository import *

def test_get_all_users(db_connection): 
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)

    users = repository.all() 

    assert users == [
        User(1, 'email1', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'username1'),
        User(2, 'email2', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', 'username2'),
        User(3, 'email3', '5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764', 'username3'),
    ]

def test_create_user(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)
    user = User(None, 'email4', 'password', 'username4')
    repository.create(user)

    users = repository.all() 
    assert users == [
        User(1, 'email1', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'username1'),
        User(2, 'email2', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', 'username2'),
        User(3, 'email3', '5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764', 'username3'),
        User(4, 'email4', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'username4')
    ]

def test_check_password(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)
    user = User(None, 'email4', 'password', 'username4')
    repository.create(user)
    assert repository.check_password('email4', 'password') == True

def test_find_by_email(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)
    assert repository.find_by_email('email1') == User(1, 'email1', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'username1')

def test_validity_checker(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)
    assert repository.validity_checker('email@gmail.com', 'Password12!') == True

def test_check_username_unique(db_connection):
    db_connection.seed("seeds/chitter_app.sql") 
    repository = UserRepository(db_connection)
    assert repository.check_username_unique('username1') == False