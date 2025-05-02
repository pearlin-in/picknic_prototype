from models.user import User

def register_user(username, password):
    if User.load(username):
        return None  # User already exists
    user = User(username, password)
    user.save()
    return user

def login_user(username, password):
    user = User.load(username)
    if user and user.password == password:
        return user
    return None