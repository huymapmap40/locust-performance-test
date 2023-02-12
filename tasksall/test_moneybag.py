from locust import HttpLocust, TaskSet, task
import base64
import random
import json

accountsJson = {
    "accounts":[
        # Adding account for testing here
        {
            "_id" : 19170,
            "uuid" : "3FA5B2CA0641494A9C502B149D4B2867"
        },       
    ]
}

accounts = accountsJson['accounts']

def jwtHeader(accountId, accountUuid):
    tokenObject = {
        "uuid": "0913dcbc96ac43dd89c49c979b87a4de",
        "iss":"web",
        "issuedAt":1492088188.859,
        "iat":1492088188,
        "exp":1692089088,
        "id": 4197246,
    }
    encodedToken = json.JSONEncoder().encode(tokenObject)
    encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
    return {
        "Authorization": 'JWT ' + str(encodedAuth, 'utf-8')
    }

class UserBehavior(TaskSet):
    @task(2)
    def charge(self):
        header = { **jwtHeader() }
        payload = {
            "withdrawalrequest": {
                "_id": "5f40e9819c41aeb3b76c5208",
                "type": "sg-sbecommerce",
                "source": "moneybag",
                "lifecycle": [
                    {
                        "state": "init",
                        "transitionedAt": "2020-08-22T09:46:41.000+0000"
                    }
                ]
            },
            "check": 1
        }
        
        self.client.post(
            "/v1/transactions/actions/charge", 
            json=payload,
            headers=header
        )   

    def on_start(self):
        position = random.randint(0, len(accounts) - 1)
        self.accountId = accounts[position]["_id"]
        self.accountUUID = accounts[position]["uuid"]

    @task(1)
    def overview(self):
        header = { **jwtHeader(self.accountId, self.accountUUID) }
        response = self.client.get("/overview/transactions", headers=header)   

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 500
