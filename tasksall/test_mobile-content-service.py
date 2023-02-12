
import json
from locust import HttpUser, TaskSet, task, between
import random
POWERSCREEN_CODE = "sbgo_food_category_healthy"
DEAL_COM_ID = "5f9248f80088516f0be87db2"
MERCHANT_RECO_COM_ID = "5ecddf090119129570ce27cd"
MERCHANT_MANUAL_COM_ID = "5f8679b12c5d83990ea062b4"
MERCHANT_AUTO_COM_ID = "5f8fbc032c5d834969a062bb"
DEAL_MANUAL_COM_ID = "5f90f3b8ef7761952676449d"
CATEGORY_ID = "60000159"


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3'
        }

    @task
    def get_products(self):
        containerId = random.choice(['5fab488aa4124af18b65f273', '5fad0d2fae92de2b9db61982', '5fbb34714eac925916e46b4b'])
        self.client.get(
            url='/mobile-content/v1/components/' + containerId,
            headers=self.headers
        )

    @task
    def get_auto_merchants(self):
        merchantId = random.choice(['5f9a2a2999096cc28d37b262', '5e90a1eddf9d1da91755fac2', '5e8dfc68df9d1dd88a55fab2'])
        self.client.get(
            url='/mobile-content/v1/component/merchants-auto/' + merchantId,
            headers=self.headers
        )

    @task
    def get_powerscreen(self):
        self.client.get(
            url=f"/mobile-content/v1/powerscreens/{POWERSCREEN_CODE}",

    def get_manual_merchants(self):
        merchantId = random.choice(['5f150d409753ca386ab6a864', '5f170190f2cf4caf4e15f490', '5f237b6418bc17bf4e89bfeb'])
        self.client.get(
            url='/mobile-content/v1/component/merchants-manual/' + merchantId,

            headers=self.headers
        )

    @task
    def get_reco_merchants(self):
        merchantId = random.choice(['601115801a931f5084d67a9e', '600fe5136cefd6651d3c9a20', '5ec376a1feb96165b4b31d0a'])
        self.client.get(
            url=f"/mobile-content/v1/components/{DEAL_COM_ID}",
            headers=self.headers
        )
    
    @task
    def get_merchants_reco(self):
        self.client.get(
            url=f"/mobile-content/v1/component/merchants-reco/{MERCHANT_RECO_COM_ID}",
            headers=self.headers
        )

    @task
    def get_merchants_manual(self):
        self.client.get(
            url=f"/mobile-content/v1/component/merchants-manual/{MERCHANT_MANUAL_COM_ID}",
            headers=self.headers
        )
    
    @task
    def get_merchants_auto(self):
        self.client.get(
            url=f"/mobile-content/v1/component/merchants-auto/{MERCHANT_AUTO_COM_ID}",
            headers=self.headers
        )
    
    @task
    def get_deals_manual(self):
        self.client.get(
            url=f"/mobile-content/v1/component/deals-manual/{DEAL_MANUAL_COM_ID}",
            headers=self.headers
        )

    @task
    def get_cat_available(self):
        self.client.get(
#            url="/component-product/v1/categories/available",
            url='/mobile-content/v1/component/merchants-reco/' + merchantId,

            headers=self.headers
        )

    @task
    def get_cat_product_active(self):
        self.client.get(
            url=f"/component-product/v1/categories/{CATEGORY_ID}/products/active",

    def get_auto_deals(self):
        dealId = random.choice(['5f291bdddb38ac1efa3fd02e', '5f33609c8cf6fd46bee33231', '5f3400350e147069877a925b'])
        self.client.get(
            url='/mobile-content/v1/component/deals-auto/' + dealId,
            headers=self.headers
        )

    @task
    def get_manual_deals(self):
        dealId = random.choice(['5f5666c64d2ebf2d275e0bf7', '5f5dfee17c2d4378e9b527d1', '5f6b19b57b71283494200e09'])
        self.client.get(
            url='/mobile-content/v1/component/deals-manual/' + dealId,
            headers=self.headers
        )

    @task
    def get_v1_groupscreen_deals(self):
        self.client.get(
            url='/mobile-content/v1/groupscreen/deals',
            headers=self.headers
        )

    @task
    def get_v2_groupscreen_deals(self):
        self.client.get(
            url='/mobile-content/v2/groupscreen/deals',
            headers=self.headers
        )

    @task
    def get_powerscreen(self):
        code = random.choice(['discoverboundbywine', 'discoverchangirecommends', 'sbgo_dbs_campaign_2020'])
        self.client.get(
            url='/mobile-content/v1/powerscreens/' + code,
            headers=self.headers
        )

    @task
    def get_component_products(self):
        cateId = random.choice([1, 3, 6, 7])
        self.client.get(
            url='/component-product/v1/categories/' + str(cateId) + '/products/active',
            headers=self.headers
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.1, 0.5)

