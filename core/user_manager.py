# Login, register, save/load user
import json
import os


def load_user(username):
    path = f"data/users/user_{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def save_user(username, data):
    os.makedirs("data/users", exist_ok=True)
    with open(f"data/users/user_{username}.json", "w") as f:
        json.dump(data, f)


def user_exists(username):
    return os.path.exists(f"data/users/user_{username}.json")
