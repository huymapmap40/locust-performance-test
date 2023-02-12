from locust import task, tag, TaskSet
import common
import random


class Scenario11(TaskSet):
    def __init__(self, parent):
        super(Scenario11, self).__init__(parent)
        self.merchants = random.choice(common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.merchant_shortname = self.merchants['MERCHANT_SHORTNAME']
        self.cookies = common.COOKIES
        self.a_link_id = None
        

    @tag('scenario11')
    @task
    def task11(self):
        self.client.get(url=f'{common.BASE_URL}/{self.merchant_shortname}',
            cookies=self.cookies,
            name=f'scenario11 - /{self.merchant_shortname}')

        merchant_response = self.client.get(
            url=f'{common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}/detail-with-affiliate-link',
            headers=common.HEADERS, name=f'scenario11 - /detail-with-affiliate-link')
        self.a_link_id = merchant_response.json()['data']['defaultAffiliateId']

        response = self.client.get(
            url=f'{common.BASE_URL}/redirect/alink/{self.a_link_id}',
            cookies=self.cookies,
            name=f'scenario11 - /redirect/alink/{self.a_link_id}'
        )