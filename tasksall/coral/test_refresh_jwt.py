import json
import base64
import sys
from locust import HttpUser, TaskSet, task
from datetime import datetime
import random

class UserBehavior(TaskSet):
    MAX_COUNT = 1600
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.play_response = {}

        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'X-Shopback-Member-Access-Token': None
        }
        self.counter = random.randint(1, 1600)
        email = "shopback.testerlocust{}@shopback.com".format(self.counter)
        payload = {
            "email": email,
            "password": "abcd1234"
        }
        response = self.client.post(url="/members/sign-in",
            headers=self.headers, json=payload)
        res = response.json()
        self.headers['X-Shopback-Member-Access-Token'] = res['userTokens']['accessToken']['id']
        self.headers['X-Shopback-JWT-Access-Token'] = res['auth']['access_token']
        self.headers['X-Shopback-Member-Refresh-Token'] = res['userTokens']['refreshToken']['id']

    @task(1)
    def refreshJwtToken(self):
        self.client.post(url="/members/me/refresh-jwt-token",
            headers=self.headers, json={})
        self.client.post(url="/members/me/refresh-access-token",
            headers=self.headers, json={})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 3000
