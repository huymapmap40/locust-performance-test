import json
import base64
import sys
from locust import HttpUser, TaskSet, task, between
from random import randint
import random
import base64
class UserBehavior(TaskSet):
    testTags = ['aa30760dc70e88063f1ffccaa89086c5', 'a5ea92da0b950de09b4ee88bc91b2c2d', '9ddd102586a8646ef7fa01c1325b0914', '9557b334642414950ad1c8e3aeeb8c68', 'd9bda5a3165f0620228293d741d97f50', '92ae09d6020e55f83ec407ab72217f2e', 'cead5d31a7741a0de8d4b2843a35a2ad']
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        accountId = randint(600011316, 600011332)
        headerStr = json.dumps({"id": accountId, "uuid": "mockuuid13fw3342fw"}).encode('utf-8')
        header = base64.b64encode(headerStr)
        base64_message = header.decode('utf-8')

        self.headers = {
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'Authorization': 'JWT ' + base64_message
        }

    @task(2)
    def getOfferRecommend(self):
        self.client.get(url="/v2/offers/recommend",
            headers=self.headers)
        self.client.close()

    @task(2)
    def getOfferRecommendWithTag(self):
        self.client.get(url="/v2/offers/recommend?tag=" + random.choice(self.testTags),
            headers=self.headers)
        self.client.close()
        
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.2)