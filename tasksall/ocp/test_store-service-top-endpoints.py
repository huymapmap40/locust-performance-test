from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/2.8.0',
            'Authorization': 'Bearer eyJpZCI6IDQ2ODg0NTN9',
            'X-Request-ID': 'f022449e-b9dd-4485-8e4d-7b6aa5e5a871',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
        }

    def on_start(self):
        if hasattr(self, 'merchants'):
            return
        merchantsResponse = self.client.get(
            url='/v1/merchants',
            headers=self.headers
        )
        self.merchants = json.loads(merchantsResponse.text)
        self.merchant = random.choice(self.merchants.get('data'))

    @task
    def merchantList(self):
        self.client.get(
            url='/v1/merchants',
            headers=self.headers
        )
        
    @task
    def merchantList(self):
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.headers
        )
        
    @task
    def merchantList(self):
        self.client.get(
            url='/v1.1/merchants',
            headers=self.headers
        )

    @task
    def merchantDetail(self):
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.headers
        )
        
    @task
    def merchantDetail(self):
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1.1/merchants/' + str(merchantId),
            headers=self.headers
        )

    @task
    def internalMerchant(self):
        self.client.get(
            url='/v1/internal/merchants',
            headers=self.headers
        )


    @task
    def categories(self):
        self.client.get(
            url='/categories/level/0',
            headers=self.headers
        )

    @task
    def banner(self):
        self.client.get(
            url='/v1/banners',
            headers=self.headers
        )

    @task
    def partnerApps(self):
        self.client.get(
            url='/mobile/partner-apps',
            headers=self.headers
        )


    @task
    def slugs(self):
        slug = self.merchant.get('shortname')
        self.client.get(
            url='/v1/slugs/' + slug,
            headers=self.headers
        )


    @task
    def merchantSearch(self):
        merchantName = self.merchant.get('name')
        self.client.get(
            url='/v1/merchants/search?q=' + str(merchantName),
            headers=self.headers
        )

    @task
    def merchantAffiliateLink(self):
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/affiliate-link',
            headers=self.headers
        )


class User(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0, 1)

