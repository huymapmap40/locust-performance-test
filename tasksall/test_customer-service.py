import json
import base64
import sys

from locust import HttpUser, TaskSet, task

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
            url="/customer/accounts/12/self-deletion/request",
            headers=self.headers
        )


class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000