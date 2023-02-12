# coding=utf-8
from locust import HttpLocust, TaskSet, task
import base64
import json
import random

USE_IRON_GATE = "true"  # string
COUNTRY = "TW"
DOMAIN = "www.shopback.com.tw"

ACCOUNT_IDS = [2478708, 2478702, 2478665, 2478662, 2478646, 2478645]

offer_ids_csv_file = 'orca_offer_ids.csv'
offer_ids_csv_file = '/locust-tasks/' + offer_ids_csv_file  # path for k8s
group_ids_csv_file = 'orca_group_ids.csv'
group_ids_csv_file = '/locust-tasks/' + group_ids_csv_file  # path for k8s

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": USE_IRON_GATE,
    "X-Shopback-Country": COUNTRY,
    "x-Shopback-domain": DOMAIN
}


def generate_jwt_tokens(account_ids):
    tokens = []
    for account_id in account_ids:
        authorization_content = json.dumps({
            "uuid": "479c94048a8e410694ea24fc17302906",
            "iss": DOMAIN,
            "issuedAt": 1577477107.184,
            "iat": 1577477107,
            "exp": 1578773107,
            "id": account_id
        })
        tokens.append(base64.b64encode(authorization_content.encode('utf-8')).decode('utf-8'))
    return tokens


class UserBehavior(TaskSet):
    tokens = generate_jwt_tokens(ACCOUNT_IDS)
    print('Tokens: {}'.format(tokens))

    with open(offer_ids_csv_file, 'r') as f:
        offer_ids = f.read().splitlines()

    with open(group_ids_csv_file, 'r') as f:
        group_ids = f.read().splitlines()

    @task(1)
    def get_unread_count(self):
        token = random.choice(self.tokens)
        headers = HEADERS.copy()
        headers['Authorization'] = 'JWT {}'.format(token)
        url = '/favorite/notification/product'
        self.client.get(url, headers=headers, name=url)

    @task(1)
    def read_count(self):
        token = random.choice(self.tokens)
        headers = HEADERS.copy()
        headers['Authorization'] = 'JWT {}'.format(token)
        url = '/favorite/notification/product/read'
        self.client.post(url, headers=headers, name=url)

    @task(1)
    def get_price_history(self):
        token = random.choice(self.tokens)
        headers = HEADERS.copy()
        HEADERS['Authorization'] = 'JWT {}'.format(token)
        offer_id = random.choice(self.offer_ids)
        self.client.get('/product/{}/price-history'.format(offer_id), headers=headers, name='/product/:id/price-history')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
