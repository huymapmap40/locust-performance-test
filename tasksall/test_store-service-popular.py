from locust import HttpUser, TaskSet, task
import random
import json

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
        }

        self.categoryIds = [2,3,4,6,7,8,11,12]
        self.categoryId = random.choice(self.categoryIds)


    @task
    def getMerchantPopulars(self):
        self.client.get(
            url='/v1/merchants/populars',
            headers=self.headers
        )

    @task
    def getMerchantPopularsByCategory(self):
        self.client.get(
            url='/v1/merchants/populars?category=' + str(self.categoryId),
            headers=self.headers
        )


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
