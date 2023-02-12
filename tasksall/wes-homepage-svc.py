from locust import HttpUser, TaskSet, task, between
import random
import json
class Scenario1(TaskSet):
    def __init__(self, parent):
        super(Scenario1, self).__init__(parent)
        self.headers = {
            'Host': 'staging.shopback.sg'
        }

    @task
    def task1(self):
        self.client.get(
            url='/',
            name='Home - Nonlogin - /'
        )
class WebsiteUser(HttpUser):
    tasks = [Scenario1]
    wait_time = between(0.05, 0.1)
