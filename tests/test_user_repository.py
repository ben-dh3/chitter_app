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