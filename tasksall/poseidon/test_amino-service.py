from locust import HttpUser, TaskSet, task
import json


class ExtensionMerchants(TaskSet):
    @task
    def extension_merchants(self):
        url = '/v1/extension/merchants'
        headers = {
            'x-shopback-irongate-enabled': 'true',
            'x-shopback-last-cc': 'SG',
            'x-shopback-domain': 'www.shopback.sg',
            'Connection': 'close'
        }
        self.client.get(
            url,
            headers = headers,
            name = 'Get Extension merchants')


class WebsiteUser(HttpUser):
    tasks =  [ExtensionMerchants]
    min_wait = 1000
    max_wait = 1000
