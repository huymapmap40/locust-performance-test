from locust import HttpLocust, TaskSet, task
import base64
import random
import json

with open('/scripts/account.json') as json_file:
    jsonData = json.load(json_file)
    accounts = jsonData['accounts']

def jwtHeader():
    position = random.randint(0, len(accounts) - 1)
    accountId = accounts[position]["_id"]
    accountUUID = accounts[position]["uuid"]
    tokenObject = {
        "uuid": accountUUID,
        "iss":"web",
        "issuedAt":1492088188.859,
        "iat":1492088188,
        "exp":1692089088,
        "id": accountId,
    }
    encodedToken = json.JSONEncoder().encode(tokenObject)
    encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
    return {
        "Authorization": 'JWT ' + str(encodedAuth, 'utf-8')
    }

class UserBehavior(TaskSet):
    @task(1)
    def overview(self):
        header = { **jwtHeader() }
        response = self.client.get("/overview/transactions", headers=header)   

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 500
