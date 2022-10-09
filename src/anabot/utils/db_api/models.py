import json


class User:
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def toJSON(self):
        return {
            'id': self.id,
            'role': self.role,
        }


class News:
    def __init__(self):
        self.id = None
        self.short_text = None
        self.url = None

    def fromJSON(self, json_file):
        news_description = json_file
        self.id = news_description['id']
        self.short_text = news_description['short_text']
        self.url = news_description['url'].split(':')[1][2:]


class Action:
    def __init__(self, user_id, post_id, action):
        self.action = action
        self.user_id = user_id
        self.post_id = post_id

    def toJSON(self):
        return {
            'id': int(self.action),
            'user_id': int(self.user_id),
            'action': self.post_id,
        }
