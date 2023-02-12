from locust import HttpUser, TaskSet, task
import random
import json


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def on_start(self):
        self.categoryIds = [1, 3, 4, 5, 7, 12, 11]
        self.categoryId = random.choice(self.categoryIds)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/2.8.0',
            'Authorization': 'Bearer eyJpZCI6IDQ2ODg0NTN9',
            'X-Request-ID': 'f022449e-b9dd-4485-8e4d-7b6aa5e5a871',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
        }

    @task
    def productActive(self):
        self.client.get(
            url='/v1/categories/'+str(self.categoryId)+'/products/active?limit=20&offset=0',
            headers=self.headers
        )

    @task
    def v2Product(self):
        self.client.get(
            url='/v2/products/available?limit=20&offset=0',
            headers=self.headers
        )

    @task
    def productCategory(self):
        self.client.get(
            url='/v1/categories/available',
            headers=self.headers
        )


class User(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 1000
