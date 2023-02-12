from locust import HttpUser, TaskSet, task, between
import random
import logging

GATEWAY_URL = 'https://gateway-staging.shopback.sg'

CREDENTIALS = {
    'email': 'roran.lai@shopback.com',
    'password': 'ShopBack123'
}
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.sg',
    'X-Shopback-Agent': 'sbconsumeragent/1.0',
    'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
    'X-Shopback-Client-User-Agent': 'Locust test',
    'X-Shopback-Recaptcha-Type': 'bypass',
    'X-shopback-internal': '682a46b19b953306c9ee2e8deb0dc210',
}

token = None


class UserBehavior(TaskSet):
    headers = {
        'Content-Type': 'application/json',
        'X-Shopback-Build': '2000599',
        'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
        'X-Shopback-Language': 'en',
        'X-Shopback-Agent': 'sbandroidagent/2.0.5',
        'X-Shopback-Recaptcha-Type': 'bypass',
        'X-Shopback-Domain': 'www.shopback.sg'
    }

    def get_token(self):
        global token
        if token is None:
            response = self.client.post(
                url=f'{GATEWAY_URL}/members/sign-in', headers=HEADERS, json=CREDENTIALS)
            token = response.json()['auth']['access_token']
        return token

    def on_start(self):
        cacheValue = "no-cache" if random.randint(0, 1) == 0 else "cache"
        self.headers.update({"Cache-Control": cacheValue})
        jwttoken = "eyJ1dWlkIjoiYTc3MjcwYzE5ZjYzNGZlZGE4ZGVlMzE3ZTFiY2Y4Y2QiLCJpc3MiOiJ3d3cuc2hvcGJhY2suc2ciLCJpc3N1ZWRBdCI6MTYyNTIxNDc5Mi42NzQsInJlZnJlc2hUb2tlbklkIjoiNjBkZWJiODY0ZDZlMmEwMDA3M2Y2MTAwIiwiaWF0IjoxNjI1MjE0NzkyLCJleHAiOjE2MjUyMTgzOTIsImlkIjo1MjEzMDYyLCJtZW1iZXJJZCI6NTIxMzA2MiwiYWxnIjoiSFMyNTYifQ"
        self.headers.update({"Authorization": "JWT " + jwttoken})
        logging.info("Testing with Cache-Control:" + cacheValue)

    @task(70)
    def get_configurations(self):
        self.client.get("/mobile/configurations", headers=self.headers)

    @task(15)
    def get_first_install_flow(self):
        self.client.get(
            "/mobile/first-install-flow?url=shopback%3A%2F%2Fcampaign%3Furl%3Dsome_lazada_campaign%26edu_flow%3Draph1_SG%0A",
            headers=self.headers)

    @task(3)
    def get_partner_apps(self):
        self.client.get(
            "/mobile/partner-apps", headers=self.headers)


class AppUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
