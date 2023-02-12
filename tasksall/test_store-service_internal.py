from locust import HttpLocust, TaskSet, task
import random
import json

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.headers_agent = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
        }

    def on_start(self):
        if hasattr(self, 'merchants'):
            return
        merchantsResponse = self.client.get(
            url='/v1/internal/merchants',
            headers=self.headers
        )
        self.merchants = json.loads(merchantsResponse.text)
        self.merchant = random.choice(self.merchants.get('data'))
        ### Deal
        dealsResponse = self.client.get(
            url='/v1/internal/deals',
            headers=self.headers
        )
        self.deals = json.loads(dealsResponse.text)
        self.deal = random.choice(self.deals.get('data'))
        ### e-outlets
        eoutletsResponse = self.client.get(
            url='/v1/internal/e-outlets',
            headers=self.headers
        )
        self.eoutlets = json.loads(eoutletsResponse.text)
        self.eoutlet = random.choice(self.eoutlets.get('data'))
        ### Stores
        storesResponse = self.client.get(
            url='/v1/internal/salmon/adm/stores',
            headers=self.headers
        )
        self.stores = json.loads(storesResponse.text)
        self.store = random.choice(self.stores.get('data'))
        ### Get Categories
        exmerchantsResponse = self.client.get(
            url='/v1/merchants',
            headers=self.headers_agent
        )
        self.exmerchants = json.loads(exmerchantsResponse.text)
        self.exmerchant = random.choice(self.exmerchants.get('data'))

    #### Get Merchants ####
    @task
    def getAllMerchant(self):
        self.client.get(
            url='/v1/internal/merchants',
            headers=self.headers
        )

    @task
    def getMerchantPublic(self):
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.headers
        )

    @task
    def getMerchantExtension(self):
        self.client.get(
            url='/v1/internal/merchants/extension',
            headers=self.headers
        )

    @task
    def getMerchantDetail(self):
        self.client.get(
            url='/v1/internal/merchants/' + str(self.merchant.get('id')),
            headers=self.headers
        )

    #### Get Deals ####
    @task
    def getAllDeals(self):
        self.client.get(
            url='/v1/internal/deals',
            headers=self.headers
        )

    @task
    def geDealDetail(self):
        self.client.get(
            url='/v1/internal/deals/' + str(self.deal.get('id')),
            headers=self.headers
        )

    #### Get e-outlets ####
    @task
    def getAllEOutlets(self):
        self.client.get(
            url='/v1/internal/e-outlets',
            headers=self.headers
        )

    @task
    def getEOutletDetail(self):
        self.client.get(
            url='/v1/internal/e-outlets/'+ str(self.eoutlet.get('id')),
            headers=self.headers
        )

    @task
    def getEOutletMaxDaySet(self):
        self.client.get(
            url='/v1/internal/e-outlets/maximum-days-pending-set',
            headers=self.headers
        )

    @task
    def getEOutletTrackInfo(self):
        self.client.get(
            url='/v1/internal/e-outlets/'+ str(self.eoutlet.get('id')) + '/tracking-information',
            headers=self.headers
        )

    @task
    def getSalmonEOutletDetail(self):
        self.client.get(
            url='/v1/internal/salmon/e-outlets/'+ str(self.eoutlet.get('id')),
            headers=self.headers
        )

    #### Get Stores ####
    @task
    def getAllStores(self):
        self.client.get(
            url='/v1/internal/salmon/adm/stores',
            headers=self.headers
        )

    @task
    def getStoreDetail(self):
        self.client.get(
            url='/v1/internal/salmon/adm/stores/'+ str(self.store.get('id')),
            headers=self.headers
        )

    @task
    def getLiveStore(self):
        self.client.get(
            url='/v1/internal/salmon/adm/live-stores',
            headers=self.headers
        )

    #### Get Categories ####
    @task
    def getCategoriesPlatform(self):
        self.client.get(
            url='/v1/internal/categories/'+ str(random.choice(self.exmerchant['categories'])) +'/platforms',
            headers=self.headers
        )

    @task
    def getCategoriesEOutlet(self):
        self.client.get(
            url='/v1/internal/salmon/categories/'+ str(random.choice(self.exmerchant['categories'])) +'/e-outlets',
            headers=self.headers
        )

    @task
    def getCategoriesMerchants(self):
        self.client.get(
            url='/v1/internal/categories/'+ str(random.choice(self.exmerchant['categories'])) +'/merchants',
            headers=self.headers
        )

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1000
