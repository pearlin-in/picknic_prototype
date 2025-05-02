import json
import os

class User:
    def __init__(self, username, password, profile_pic='', memories=None):
        self.username = username
        self.password = password
        self.profile_pic = profile_pic
        self.memories = memories or []

    @classmethod
    def load(cls, username):
        filename = f"user_{username}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return cls(
                    username=data['username'],
                    password=data['password'],
                    profile_pic=data.get('profile_pic', ''),
                    memories=data.get('memories', [])
                )
        return None

    def save(self):
        data = {
            "username": self.username,
            "password": self.password,
            "profile_pic": self.profile_pic,
            "memories": self.memories
        }
        with open(f"user_{self.username}.json", 'w') as f:
            json.dump(data, f)