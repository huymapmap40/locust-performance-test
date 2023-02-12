import json
import base64
import sys

from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.play_response = {}

        access_token = 'JWT ' + self.generate_jwt_token()
        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'Authorization': access_token
        }

    def generate_jwt_token(self):
        json_obj = {
            'uuid': '0c4fbbc97da24b52a81ffe0da4c86acf',
            'iss': 'web',
            'issuedAt': 1492088188.859,
            'iat': 1492088188,
            'exp': 1692089088,
            'id': 313134
        }

        encoded_token = json.JSONEncoder().encode(json_obj)
        encoded_auth = base64.b64encode(encoded_token.encode("utf-8"))

        # access_token = str(encoded_auth).encode('utf-8')
        access_token = str(encoded_auth, 'utf-8')

        return access_token

    @task
    def get_profile(self):
        self.client.get(
            url="/game/v1/profiles/mine",
            headers=self.headers
        )

    @task
    def get_history_prizes(self):
        self.client.get(
            url='/game/v1/history-prizes/mine?limit=30&offset=0',
            headers=self.headers
        )

    @task
    def get_history_boards(self):
        self.client.get(
            url='/game/v1/history-boards/mine/troopers?limit=30&offset=0',
            headers=self.headers
        )

    @task
    def get_diamonds_by_prizes(self):
        self.client.get(
            url='/game/v1/profiles/313134/prizes/get-diamonds',
            headers=self.headers
        )

    @task
    def play(self):
        payload = {
            "gameId": "troopers"
        }

        self.play_response = self.client.post(
            url='/game/v1/play',
            headers=self.headers,
            json=payload
        )

        if self.play_response:
           if 'transactionId' in self.play_response.text:
              res = self.play_response.json()
              tran = res['data']['transactionId']
           else:
              return
        else:
           return

        payload = {
            "transactionId": tran,
            "points": 3000,
            "gameId": "troopers",
            "gameData": [3, 5, 1, 1, 1, 1, 1, 1, 1, 1]
        }

        self.headers['x-hash'] = 'un67YrmExbuX2rIO+nfjQzlyEY8='
        self.headers['x-random-string'] = '5794355a3a8d6b6'
        self.headers['x-no-hash'] = 'xxx.shopb@ck.n0h@sh.xxx'

        self.play_response_end = self.client.post(
            url='/game/v1/gl/end',
            headers=self.headers,
            json=payload
        )
        print("Payload: " + json.dumps(payload) + " Response: " + self.play_response_end.text)

    @task
    def debit_diamonds_start(self):
        payload = {
            "diamondsDebit": 1,
            "prizeName": "load test",
            "prizeTx": "prizeTx testing"
        }

        self.client.post(
            url='/game//v1/profiles/313134/prizes/debit-diamonds-start',
            headers=self.headers,
            json=payload
        )


class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.1, 0.2)