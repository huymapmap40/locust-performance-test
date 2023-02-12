from locust import HttpUser, TaskSet, task
import random
import json

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.ebay = {
            'id': '9472',
            'slug': 'booking-com',
            'eOutletId': '14'
        }
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
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

        dealsResponse = self.client.get(
            url='/v1/merchants/8440/deals',
            headers=self.headers
        )
        self.deals = json.loads(dealsResponse.text)
        self.deal = random.choice(self.deals.get('data'))

#    @task
#    def getAllMerchant(self):
#        self.client.get(
#            url='/v1/merchants',
#            headers=self.headers
#        )

    @task
    def getSlug(self):
        shortname = self.merchant.get('shortname')
        if shortname is None:
            return
        self.client.get(
            url='/v1/slugs/' + shortname,
            headers=self.headers
        )

    @task
    def getPopularMerchants(self):
        self.client.get(
            url='/v1/merchants/populars',
            headers=self.headers
        )

    @task
    def getUpsizeMerchants(self):
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.headers
        )

    @task
    def getTrendingMerchants(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')) + '/trendings',
            headers=self.headers
        )

    @task
    def getMerchantBanners(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')) + '/banners',
            headers=self.headers
        )

    @task
    def getMerchantDetail(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')),
            headers=self.headers
        )

    @task
    def getDeals(self):
        self.client.get(
            url='/v1/deals/' + str(self.deal.get('id')),
            headers=self.headers
        )

    @task
    def getMerchantSimilarDeals(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')) + '/similar-deals',
            headers=self.headers
        )

    @task
    def getMerchantSimilar(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')) + '/similars',
            headers=self.headers
        )

    @task
    def getMerchantRating(self):
        self.client.get(
            url='/v1/merchants/' + str(self.merchant.get('id')) + '/rating',
            headers=self.headers
        )

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
