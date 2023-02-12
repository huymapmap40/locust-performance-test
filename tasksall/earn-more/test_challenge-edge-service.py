import json
import base64
import random

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def getUserHeaders(self, user, uuid = ''):
        account = '{"id":'+ str(user) + ',"uuid":"' + uuid + '"}'
        encodedBytes = base64.b64encode(account.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        headers ={
            "Authorization": 'Bearer ' + encodedStr,
            "X-Shopback-Agent": "sbandroidagent/3.41.1",
            "X-Shopback-Build": "3410199"
        }
        return headers

    def getRandomUserHeaders(self):
        ran = random.randint(1000000000, 2000000000)
        return self.getUserHeaders(ran)

    def getPreDefinedUsersHeaders(self):
        return self.getUserHeaders(5213064, 'bbd40d5ca92e4eff9360e0e2d25f65f6')

    @task(1)
    def challengeHomeLayout(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/home-layout',
            headers=headers
        )

    @task(20)
    def getDiscoveryGroupCodeChallenge(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/discovery-group-challenges/P1',
            headers=headers
        )

    @task(5)
    def challengeHomeLayout(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/home-layout',
            headers=headers
        )

    @task(5)
    def getChallengeProgressComponent(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/challenge-progress-component',
            headers=headers
        )

    @task(5)
    def getMicroActionChallenge(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/micro-action-challenges',
            headers=headers
        )

    @task(5)
    def getUnrevealedRewards(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/unrevealed-rewards',
            headers=headers
        )

    @task(1)
    def getDiscoveryGroupChallenge(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/discovery-group-challenges',
            headers=headers
        )


    @task(1)
    def getInProgressChallenges(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/in-progress-challenges',
            headers=headers
        )

    @task(1)
    def getChallengeHistory(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v5/challenge-history?filterType=ALL',
            headers=headers
        )


class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
