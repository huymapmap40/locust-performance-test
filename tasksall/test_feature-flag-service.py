import json
import base64

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
            "X-Shopback-Build": "3280000",
            "X-Shopback-Agent": "sbiosagent/2.2.1",
            "X-Shopback-Domain": "www.shopback.sg",
        }
        return headers

    def getPreDefinedUsersHeaders(self):
        accountId = 679024
        return self.getUserHeaders(accountId)

    @task(1)
    def loadConfiguration(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url="/feature-flag/app-reward/v1/configurations",
            headers=headers
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
