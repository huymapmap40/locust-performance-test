from locust import task, tag, TaskSet
import common
import random


class Scenario7(TaskSet):
    def __init__(self, parent):
        super(Scenario7, self).__init__(parent)
        self.merchants = random.choice(common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.merchant_shortname = self.merchants['MERCHANT_SHORTNAME']
        self.campaign = common.CAMPAIGN
        self.cookies = common.COOKIES


    @tag('scenario7')
    @task
    def task7(self):
        self.client.get(url=f'{common.BASE_URL}/{self.campaign}',
                        cookies=self.cookies,
                        name=f'scenario7 - /{self.campaign}')

        merchant_response = self.client.get(
            url=f'{common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}',
            headers=common.HEADERS, name=f'Scenario7 - /detail-with-affiliate-link')
        self.merchant_shortname = merchant_response.json()['data']['shortname']

        self.client.get(url=f'{common.BASE_URL}/{self.merchant_shortname}', headers=common.HEADERS,
                        name=f'Scenario7 - /{self.merchant_shortname}')
