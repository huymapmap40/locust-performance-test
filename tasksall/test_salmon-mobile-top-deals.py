from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.mobile_headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Domain': 'www.shopback.com.tw',
        }
        
    @task
    def getMobileTopDeals(self):
        self.client.get(
            url='/mobile/top-deals',
            headers=self.mobile_headers,
        )
   


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(10, 50)
