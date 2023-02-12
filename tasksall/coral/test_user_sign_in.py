import json
import base64
import sys
import uuid
from locust import HttpUser, TaskSet, task
from datetime import datetime
import time

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.play_response = {}
        self.counter = 0
        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'X-Shopback-Member-Ip-Address': '202.39.237.203'
        }
    @task(1)
    def signIn(self):
        email = "shopback.testerlocust{}@shopback.com".format(self.counter % 53)
        self.counter = self.counter + 1
        payload = {
            "email": email,
            "password": "abcd1234",
        }
        self.client.post(url="/members/sign-in",
                        headers=self.headers, json=payload)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 300
    max_wait = 1000