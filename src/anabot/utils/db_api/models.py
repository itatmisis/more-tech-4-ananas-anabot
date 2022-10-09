import json


class User:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def toJSON(self):
        return json.dumps({
            'id': self.id,
            'role': self.role,
        })


class News:
    def __init__(self):
        self.id = None
        self.text = None
        self.link = None
        self.photo = None

    def fromJSON(self, json_file):
        news_description = json.load(json_file)
        self.id = news_description['id']
        self.text = news_description['text']
        self.link = news_description['link'].split(':')[1]
        self.photo = news_description['photo']


class Action:
    def __init__(self, user_id, post_id, action):
        self.user_id = user_id
        self.post_id = post_id
        self.action = action

    def toJSON(self):
        return json.dumps({
            'user_id': self.user_id,
            'post_id': self.post_id,
            'action': self.action,
        })
