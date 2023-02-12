from locust import task, tag, TaskSet
import common
import random


class Scenario3(TaskSet):
    def __init__(self, parent):
        super(Scenario3, self).__init__(parent)
        self.merchants = random.choice(common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.cookies = common.COOKIES
        self.campaign = common.CAMPAIGN
        self.a_link_id = random.choice(
            [336544, 323576, 333265, 326404, 133784])

    @tag('scenario3')
    @task
    def task3(self):
        self.client.get(url=f'{common.BASE_URL}',
                        cookies=self.cookies,
                        name=f'Scenario3 - homepage')

        response = self.client.get(
            url=f'{common.BASE_URL}/redirect/alink/' + str(self.a_link_id),
            cookies=self.cookies,
            name=f'Scenario3 - /redirect/alink/{self.a_link_id}'
        )
