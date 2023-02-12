from locust import task, tag, TaskSet
import westeros_common
import random


class Scenario5(TaskSet):
    def __init__(self, parent):
        super(Scenario5, self).__init__(parent)
        self.cookies = westeros_common.COOKIES
        self.merchants = random.choice(westeros_common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.merchant_shortname = None
        self.campaign = westeros_common.CAMPAIGN

    @tag('Scenario5')
    @task
    def task5(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.campaign}',
                        cookies=self.cookies,
                        name=f'Scenario5 - /{self.campaign}')

        merchant_response = self.client.get(
            url=f'{westeros_common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}',
            headers=westeros_common.HEADERS,
            name=f'Scenario5 - /campaign/merchants/{self.merchant_id}'
        )
        self.merchant_shortname = merchant_response.json()['data']['shortname']
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.merchant_shortname}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario5 - /{self.merchant_shortname}')
