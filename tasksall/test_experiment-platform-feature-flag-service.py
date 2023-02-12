import json
import base64

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def getPreDefinedUsersPayload(self):
        accountId = 679024
        payload = {
            "flagKeys": ["test-brew-91"],
            "userId": accountId,
            "deviceId": "web_VybOEk4voxhQxory1vF0eeHC9HX9rRIM_1654089497845",
            "userProperties": {
                "androidVersion": 12345,
                "iosVersion": 2345,
            }
        }
        return payload

    @task
    def loadConfiguration(self):
        payload = self.getPreDefinedUsersPayload()
        self.client.post(url="/experiment/evaluate", json=payload)


class WebsitUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 1000
