from locust import task, tag, TaskSet
import common
import random


class Scenario8(TaskSet):
    def __init__(self, parent):
        super(Scenario8, self).__init__(parent)
        self.merchants = random.choice(common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.a_link_id = None
        self.campaign = common.CAMPAIGN
        self.cookies = common.COOKIES

    @tag('scenario8')
    @task
    def task8(self):
        self.client.get(url=f'{common.BASE_URL}/{self.campaign}',
                        cookies=self.cookies,
                        name=f'Scenario2 - /{self.campaign}')

        merchant_response = self.client.get(
            url=f'{common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}/detail-with-affiliate-link',
            headers=common.HEADERS,
            name='Scenario8 - /detail-with-affiliate-link'
        )
        self.a_link_id = merchant_response.json()['data']['defaultAffiliateId']

        response = self.client.get(
            url=f'{common.BASE_URL}/redirect/alink/{self.a_link_id}',
            cookies=self.cookies,
            name=f'Scenario6 - /redirect/alink/{self.a_link_id}'
        )