import json
import base64
import random

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def getUserHeaders(self, user):
        account = '{"id":'+ str(user) +'}'
        encodedBytes = base64.b64encode(account.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        headers ={
            "Authorization": encodedStr,
        }
        return headers

    def getRandomUserHeaders(self):
        ran = random.randint(1000000000, 2000000000)
        return self.getUserHeaders(ran)

    @task(1)
    def rewardDetails(self):
        headers = self.getRandomUserHeaders()
        self.client.get(
            url="/v1/reward/vouchers/display?campaignCode=loadtest",
            headers=headers
        )

    @task(1)
    def rewardListing(self):
        headers = self.getRandomUserHeaders()
        self.client.get(
            url='/v1/reward/vouchers/list?offset=0&limit=20',
            headers=headers
        )

    @task(1)
    def redeemVouchers(self):
        headers = self.getRandomUserHeaders()
        payload = {
            'campaignCode': 'loadtest'
        }
        self.client.post(
            url='/v1/reward/vouchers/link-to-user',
            headers=headers,
            json=payload
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
