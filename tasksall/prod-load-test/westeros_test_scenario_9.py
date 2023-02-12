from locust import task, tag, TaskSet
import westeros_common
import random

class Scenario9(TaskSet):
    def __init__(self, parent):
        super(Scenario9, self).__init__(parent)
        self.merchants = random.choice(common.MERCHANT)
        self.merchant_id = self.merchants['MERCHANT_ID']
        self.merchant_shortname = self.merchants['MERCHANT_SHORTNAME']
        self.cookies = westeros_common.COOKIES

    @tag('scenario9')
    @task
    def task9(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.merchant_shortname}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /{self.merchant_shortname}')
        self.client.get(url=f'/v1/merchants/{self.merchant_id}/banners',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /v1/merchants/{self.merchant_id}/banners')
        self.client.get(url=f'/v1/tncs?storeId={self.merchant_id}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /v1/tncs?storeId={self.merchant_id}')
        self.client.get(url=f'/v1/merchants/{self.merchant_id}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /v1/merchants/{self.merchant_id}')
        self.client.get(url=f'/mobile-content/v1/groupscreen/deals?merchantId={self.merchant_id}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /mobile-content/v1/groupscreen/deals?merchantId={self.merchant_id}')
        self.client.get(url=f'/v1/merchants/{self.merchant_id}/deals/expired',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario9 - /v1/merchants/{self.merchant_id}/deals/expired')
