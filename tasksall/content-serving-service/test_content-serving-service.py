import os
import json
import base64
import time
import random

from pathlib import Path

from locust import HttpUser, TaskSet, task, between


COUNTRY_CODE = 'TW'
DOMAIN = 'www.shopback.com.tw'
API_GATEWAY = 'http://gateway-staging.shopback.com.tw'

#COUNTRY_CODE = 'SG'
#DOMAIN = 'www.shopback.sg'
#API_GATEWAY = 'http://gateway-staging.shopback.com.sg'


def make_headers(jwt=None, **kwargs):
    sb_agent = random.choice(['sbconsumeragent/1.0', 'sbiosagent/1.0', 'sbandroidagent/1.0'])
    headers = {
        'X-Shopback-Agent': sb_agent,
        'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
        'X-Shopback-Store-Service': 'true',
        'X-Shopback-Country': COUNTRY_CODE,
        'X-Shopback-Domain': DOMAIN,
        'X-Shopback-Build': '99999999',
    }
    if kwargs:
        headers.update(kwargs)
    if jwt:
        headers['Authorization'] = f'JWT {jwt}'
    return headers


def make_jwt(account_id, uuid):
    iat = int(time.time()) - 3600
    auth = json.dumps({
        'uuid': uuid,
        'iss': DOMAIN,
        'issuedAt': iat,
        'iat': iat,
        'exp': iat + (3600 * 24),
        'id': account_id,
    })
    return base64.b64encode(auth.encode('utf-8')).decode('utf-8')


class Tasks(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.available_tokens = self.load_tokens('available_users.jsonlines')
        self.available_layouts = self.load_jsonlines('available_layouts.jsonlines')
        self.available_components = self.load_jsonlines('available_components.jsonlines')

    def load_jsonlines(self, filename):
        with Path(os.path.dirname(__file__), filename).open() as file:
            return [json.loads(line.strip()) for line in file]

    def load_tokens(self, filename):
        users = self.load_jsonlines(filename)
        return list(map(lambda x: make_jwt(**x), users))

    @task()
    def get_layout(self):
        layout = random.choice(self.available_layouts)
        self.client.get(
            url=f'/v1/layouts/{layout["type"]}/{layout["identifier"]}',
            headers=make_headers(),
            name=f'layout-{layout["identifier"]}',
        )

    @task()
    def get_layout_by_login_user(self):
        layout = random.choice(self.available_layouts)
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url=f'/v1/layouts/{layout["type"]}/{layout["identifier"]}',
            headers=make_headers(jwt=jwt),
            name=f'layout-{layout["identifier"]}-login-user',
        )

    @task()
    def get_experiment_layout_by_login_user(self):
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url='/v1/layouts/home/load-test-experiment-layout',
            headers=make_headers(jwt=jwt),
            name='experiment-layout',
        )

    @task()
    def get_layout_see_more(self):
        component = random.choice(self.available_components)
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url=f'/v1/layouts/see-more/{component["id"]}',
            headers=make_headers(jwt=jwt),
            name=f'layout-see-more-{component["id"]}',
        )

    @task()
    def get_component_content(self):
        component = random.choice(self.available_components)
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url=f'/v1/components/{component["id"]}/content',
            headers=make_headers(jwt=jwt),
            name=f'component-content-{component["id"]}',
        )

    @task()
    def get_component_content_banner_set(self):
        component = random.choice(self.available_components)
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url=f'/v1/components/{component["id"]}/content/banner-set',
            headers=make_headers(jwt=jwt),
            name=f'component-content-banner-set-{component["id"]}',
        )

    @task()
    def get_component_content_see_more(self):
        component = random.choice(self.available_components)
        jwt = random.choice(self.available_tokens)
        self.client.get(
            url=f'/v1/components/{component["id"]}/content/see-more',
            headers=make_headers(jwt=jwt),
            name=f'component-content-see-more-{component["id"]}',
        )


class WebsiteUser(HttpUser):
    tasks = [Tasks, ]
    wait_time = between(1, 3)
