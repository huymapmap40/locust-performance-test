from locust import HttpUser, TaskSet, task
import base64
import random
import json
from dataprovider import *

def jwtHeader(accountId):
    tokenObject = {
        "id": accountId,
    }
    encodedToken = json.JSONEncoder().encode(tokenObject)
    encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
    return {
        "Authorization": 'JWT ' + str(encodedAuth, 'utf-8')
    }

class UserBehavior(TaskSet):
    def on_start(self):
      self.accountId = random.choice(ACCOUNTS)
   
    @task(1)
    def overview(self):
        header = { **jwtHeader(self.accountId) }
        response = self.client.get("/overview/transactions", headers=header)   

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1500

