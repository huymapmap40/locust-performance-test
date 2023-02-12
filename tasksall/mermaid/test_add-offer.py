import json
import base64
import sys
from locust import HttpUser, TaskSet, task, between
from random import randint
import base64

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        accountId = randint(600011316, 630000000)
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

    @task(1)
    def addOffer(self):
        offerId = randint(18733, 20158)
        payload = {}
        self.client.post(url="/offer/follow/" + str(offerId),
            headers=self.headers, json=payload)
        self.client.close()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.2)
