class Post:
    def __init__(self, id, message, time, user_id, username = ''):
        self.id = id
        self.message = message
        self.time = time
        self.user_id = user_id
        self.username = username

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Post({self.id}, {self.message}, {self.time}, {self.user_id})"