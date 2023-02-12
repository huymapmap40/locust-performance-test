import json
from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.com.au',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3'
        }


    @task
    def get_category(self):
        self.client.get(
            url='/categories/level/0',
            headers=self.headers
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000

