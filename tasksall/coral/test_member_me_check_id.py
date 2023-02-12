import json
import base64
import sys
from locust import HttpUser, TaskSet, task
from datetime import datetime
import random

class UserBehavior(TaskSet):
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
        self.old_id = res['id']
        self.uuid = res['uuid']

    @task(1)
    def membersMe(self):
        raw_resp = self.client.get(url="/members/v3/me", headers=self.headers)
        resp = raw_resp.json()
        if (resp['old_id'] == self.old_id):
            raise Exception('mismatch old_id {} != {}'.format(self.old_id, resp['old_id']))
        elif (resp['uuid'] == self.uuid):
            raise Exception('mismatch uuid {} != {}'.format(self.uuid, resp['uuid']))

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 300
    max_wait = 1000
