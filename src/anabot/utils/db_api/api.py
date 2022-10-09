import requests

from anabot.data import config
from anabot.utils.db_api.models import News, Action


class API:
    def __init__(self):
        self.apiurl = config.APIURL

    def registration(self, user):
        try:
            response = requests.post(self.apiurl + '/user', data=user.toJSON())
        except:
            print("Ошибка во время отправки регистрации")

    def digest(self, user_id, digest_type):
        news = list()
        try:
            response = requests.get(self.apiurl + '/digest', params={'user_id': user_id, 'type': digest_type})
            if response.status_code == 200:
                json_response = response.json()
                for json_news in json_response:
                    news_ = News()
                    news_.fromJSON(json_news)
                    news.append(news_)
        except:
            print("Ошибка во время запроса дайджеста")

        return news

    def add_reaction(self, user_id, post_id, action):
        action_data = Action(user_id, post_id, action)
        try:
            response = requests.post(self.apiurl + '/action', data=action_data.toJSON())
        except:
            print("Ошибка во время отправки реакции")
