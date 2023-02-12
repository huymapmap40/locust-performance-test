import random
from locust import HttpUser, TaskSet, task
from cashback_engine_dataprovider import *
import json, logging, sys, base64, datetime, uuid

# Note: Data resides in external files [data,pushdevices,accounts,default]. 
class UserBehavior(TaskSet):

    def on_start(self):
      self.accountId = random.choice(ACCOUNTS)
      self.accountUuid = 'some-random-uuid'

    def get_authorization(self):
        tokenObject = {
            "iss":"web",
            "issuedAt":1492088188.859,
            "iat":1492088188,
            "exp":1692089088,
            "id": self.accountId
        }
        encodedToken = json.JSONEncoder().encode(tokenObject)
        encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
        return 'JWT ' + str(encodedAuth, "utf-8")

    @task
    def get_overview_cashbacks(self):
        url = '/overview/cashbacks' 
        headers = {
          'Authorization' : self.get_authorization(),
          'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210',
          'X-Shopback-Agent': 'sbconsumeragent'
        }

        self.client.get(url,
            headers = headers,
            name = 'Get Overview Cashbacks to display the users balance'
        )

        logging.info(
            'GET User with accountID: %s\n and accountUuID: %s\n and Authorization token: %s\n',
            self.accountId, self.accountUuid, headers['Authorization']
        )

    #GET '/cashbacks/latest'
    @task
    def get_latest_cashbacks(self):
        url = '/cashbacks/latest'
        headers = {
          'Authorization' : self.get_authorization(),
          'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210',
          'X-Shopback-Agent': 'sbconsumeragent'
        }
        self.client.get(url,
            headers = headers,
            name = 'Get latest cashbacks when the user opens the mobile app'
        )

        logging.info(
            'GET Latest cashbacks for user with accountId: %s\n',
            self.accountId
        )


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 100
    max_wait = 500