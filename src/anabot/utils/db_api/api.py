import requests

from anabot.data import config
from anabot.utils.db_api.models import News, Action


class API:
    def __init__(self):
        self.apiurl = config.APIURL

    def registration(self, user):
        try:
            print(user.id)
            print(user.toJSON())
            response = requests.post(self.apiurl + '/users/', json=user.toJSON())
            print(response)
        except:
            print("Ошибка во время отправки регистрации")

    def digest(self, user_id, digest_type):
        news = list()
        try:
            # response = requests.get(self.apiurl + f'/news/user/{user_id}/', params={'user_id': user_id, 'type': digest_type})
            response = requests.get(self.apiurl + f'/news/user/{user_id}/')
            print(response.status_code)
            if response.status_code == 200:
                json_response = response.json()
                # print(json_response)
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
            response = requests.post(self.apiurl + '/actions/', json=action_data.toJSON())
        except:
            print("Ошибка во время отправки реакции")
