import json
import base64

from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

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

        access_token = str(encoded_auth, 'utf-8')

        return access_token

    @task(2)
    def display(self):
        self.client.get(
            url="/v1/reward/vouchers/display?campaignCode=C00001",
            headers=self.headers
        )

    @task(2)
    def list(self):
        self.client.get(
            url='/v1/reward/vouchers/list?offset=0&limit=20',
            headers=self.headers
        )

    @task(4)
    def add_voucher(self):
        payload = {
            'sbVoucherCode': 'SV00001'
        }

        self.client.post(
            url='/v1/reward/vouchers/add-voucher',
            headers=self.headers,
            json=payload
        )

    @task(4)
    def link_to_user(self):
        payload = {
            'campaignCode': 'C00001'
        }

        self.client.post(
            url='/v1/reward/vouchers/link-to-user',
            headers=self.headers,
            json=payload
        )

    @task(2)
    def check_pin_v2(self):
        payload = {
            'voucherId': '5d244d044d824beced6681bc',
            'pinCode': '123456'
        }

        self.client.post(
            url='/v2/reward/vouchers/check-pin',
            headers=self.headers,
            json=payload
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000

