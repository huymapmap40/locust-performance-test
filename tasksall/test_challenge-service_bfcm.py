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

    def getPreDefinedUsersHeaders(self):
        accountIds = [679024, 728242, 1052469, 474104, 980255, 1060589, 1364895, 1312578, 1354700, 732608, 657797, 520959, 1209574, 697497]
        accountId = random.choice(accountIds)
        return self.getUserHeaders(accountId)

    @task(1)
    def challengeHomeList(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url="/v2/challenges/current-challenges?offset=0&limit=50&sortBy=rank",
            headers=headers
        )

    @task(1)
    def challengeDetail(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/v2/challenges/LOADTEST_1010',
            headers=headers
        )

    # This test will affect data so please consider when run on PROD env
    @task(1)
    def optInChallenge(self):
        headers = self.getRandomUserHeaders()
        self.client.post(
            url='/v2/challenges/LOADTEST_1010/opt-in',
            headers=headers
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
