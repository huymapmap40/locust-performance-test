# coding=utf-8
from locust import HttpLocust, TaskSet, task
import base64
import json
import random

USE_IRON_GATE = "true"  # string
COUNTRY = "TW"
DOMAIN = "www.shopback.com.tw"

ACCOUNT_ID = random.randint(1, 100)

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


def generate_jwt_token(account_id):
    authorization_content = json.dumps({
        "uuid": "479c94048a8e410694ea24fc17302906",
        "iss": DOMAIN,
        "issuedAt": 1577477107.184,
        "iat": 1577477107,
        "exp": 1578773107,
        "id": account_id
    })
    return base64.b64encode(authorization_content.encode('utf-8')).decode('utf-8')


class UserBehavior(TaskSet):
    with open(offer_ids_csv_file, 'r') as f:
        offer_ids = f.read().splitlines()

    with open(group_ids_csv_file, 'r') as f:
        group_ids = f.read().splitlines()

    product_ids = offer_ids + group_ids
    random.shuffle(product_ids)

    user_status = {
        'action': 'put',
        'favorite_ids': [],
        'product_ids': product_ids
    }

    token = generate_jwt_token(ACCOUNT_ID)
    print('Token: ', token)
    HEADERS['Authorization'] = 'JWT {}'.format(token)

    @task(1)
    def favorite(self):
        favorite_count = len(self.user_status['favorite_ids'])
        if favorite_count < 100:
            self.user_status['action'] = 'put'
        elif favorite_count > 1500:
            self.user_status['action'] = 'delete'
            random.shuffle(self.user_status['favorite_ids'])
            print('Shuffle favorite')
            print(self.user_status['favorite_ids'])

        if self.user_status['action'] == 'put':
            product_id = self.user_status['product_ids'].pop()
            self.put_favorite(product_id)
            self.user_status['favorite_ids'].append(product_id)
        else:
            favorite_id = self.user_status['favorite_ids'].pop()
            self.remove_favorite(favorite_id)
            self.user_status['product_ids'].append(favorite_id)

        print('accountId: {}, count of favorite: {}, action: {}'.format(ACCOUNT_ID, favorite_count, self.user_status['action']))
        print(self.user_status['favorite_ids'])

    def put_favorite(self, product_id):
        if product_id in self.group_ids:
            _from = random.choice(['search', 'comparison_group'])
        else:
            _from = random.choice(['search', 'comparison_offer', 'offer_detail'])

        url = '/favorite/product/{}'.format(product_id)
        payload = json.dumps({
            "from": _from,
            "notifiedPrice": 0,
        })
        print('PUT {} {}'.format(url, payload))
        self.client.put(url, headers=HEADERS, data=payload, name='/favorite/product/:id')

    def remove_favorite(self, product_id):
        url = '/favorite/product/{}'.format(product_id)
        print('DELETE {}'.format(url))
        self.client.delete(url, headers=HEADERS, name='/favorite/product/:id')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
