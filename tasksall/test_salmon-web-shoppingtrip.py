from locust import HttpLocust, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
        }

    @task
    def webShoppingTrip(self):
        availableStores = [
            {"id": 40453, "storeId": 2281},
            {"id": 40845, "storeId": 2283},
            {"id": 36364, "storeId": 2166},
            {"id": 26246, "storeId": 1789},
            {"id": 32966, "storeId": 1804}
        ]
        store = random.choice(availableStores)
        payload = {
            'accountId': 2464051,
            'storeId': store["storeId"],
            'storeaffiliateId': store["id"],
            'browserName': 'Chrome',
            'browserVersion': 84,
            'browserPlatform': 'Mac'
        }

        self.client.post(
            url='/int/shoppingtrips',
            headers=self.headers,
            json=payload
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 10)
