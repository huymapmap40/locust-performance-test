from locust import task, tag, TaskSet
import westeros_common
import random


class Scenario6(TaskSet):
    def __init__(self, parent):
        super(Scenario6, self).__init__(parent)
        self.merchants = random.choice(westeros_common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.a_link_id = None
        self.campaign = westeros_common.CAMPAIGN
        self.cookies = westeros_common.COOKIES

    @tag('scenario6')
    @task
    def task6(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.campaign}',
                        cookies=self.cookies,
                        name=f'scenario6 - /{self.campaign}')

        merchant_response = self.client.get(
            url=f'{westeros_common.BASE_URL}/wes-api/campaign/merchants/{self.merchant_id}/detail-with-affiliate-link',
            headers=westeros_common.HEADERS, name=f'Scenario6 - /detail-with-affiliate-link')
        self.a_link_id = merchant_response.json()['data']['defaultAffiliateId']
        # no need to test redirect
        # response = self.client.get(
        #     url=f'{westeros_common.BASE_URL}/redirect/alink/{self.a_link_id}',
        #     cookies=self.cookies,
        #     name=f'Scenario6 - /redirect/alink/{self.a_link_id}'
        # )
