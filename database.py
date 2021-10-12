from flask_login import UserMixin


users = {}


class User(UserMixin):
    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def __repr__(self):
        return f'id={self.id}, name={self.name}'


def get_user_by_password(password):
    if password == '1':
        user = User('1000', 'Authenticated User')
        users[user.id] = user
        return user
    elif password == '2':
        user = User('2000', 'New User 2000')
        users[user.id] = user
        return user
    return None


def get_user_by_id(user_id):
    user = users.get(user_id, None)
    return user
