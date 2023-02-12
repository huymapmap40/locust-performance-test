from locust import task, tag, TaskSet
import westeros_common
import random


class Scenario12(TaskSet):
    def __init__(self, parent):
        super(Scenario12, self).__init__(parent)
        self.merchants = random.choice(westeros_common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.merchant_shortname = self.merchants['MERCHANT_SHORTNAME']
        self.cookies = westeros_common.COOKIES
        self.a_link_id = None

    @tag('scenario12')
    @task
    def task12(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.merchant_shortname}',
            cookies=self.cookies,
            name=f'scenario12 - /{self.merchant_shortname}')

        merchant_response = self.client.get(
            url=f'{westeros_common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}/detail-with-affiliate-link',
            headers=westeros_common.HEADERS, name=f'scenario12 - /detail-with-affiliate-link')
        self.a_link_id = merchant_response.json()['data']['defaultAffiliateId']
        # no need to run redirect
        # response = self.client.get(
        #     url=f'{westeros_commonBASE_URL}/redirect/alink/{self.a_link_id}',
        #     cookies=self.cookies,
        #     name=f'scenario12 - /redirect/alink/{self.a_link_id}'
        # )