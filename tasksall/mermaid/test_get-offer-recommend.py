import json
import base64
import sys
from locust import HttpUser, TaskSet, task, between
from random import randint
import base64
class UserBehavior(TaskSet):
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
    def getOfferByIdRecommend(self):
        offerId = randint(27732, 29734)
        # offerId = randint(27732, 27740)
        self.client.get(url="/v2/offers/" + str(offerId) + "/recommend",
            headers=self.headers)
        self.client.close()
        
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.2)