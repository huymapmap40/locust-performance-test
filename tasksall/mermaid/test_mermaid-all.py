import json
from locust import HttpUser, TaskSet, task, between
from random import randint
import base64
class UserBehavior(TaskSet):

    offers_range = (99711, 103791)
    account_range = (650000001, 650000050)

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        accountId = randint(*self.account_range)
        headerStr = json.dumps({"id": accountId, "uuid": "mockuuid13fw3342fw"}).encode('utf-8')
        header = base64.b64encode(headerStr)
        base64_message = header.decode('utf-8')

        self.headers = {
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'Authorization': 'JWT ' + base64_message
        }

    # @task(5)
    # def getOfflineScreen(self):
    #     self.client.get(url="/v2/offline-screen",
    #         headers=self.headers)
    #     self.client.close()

    # @task(5)
    # def getOffersByMerchantId(self):
    #     self.client.get(url="/v2/offers?merchantId=2&size=30",
    #         headers=self.headers)
    #     self.client.close()

    # @task(5)
    # def getOffersByLabelId(self):
    #     self.client.get(url="/v2/offers?labelId=4&size=30",
    #         headers=self.headers)
    #     self.client.close()

    # @task(5)
    # def getRecommendation(self):
    #     self.client.get(url="/v2/offers/recommend",
    #         headers=self.headers)
    #     self.client.close()

    #@task(1)
    #def getReceiptHistory(self):
    #    self.client.get(url="/receipt/history",
    #        headers=self.headers)

    # @task(1)
    # def getOfferById(self):
    #     offerId = randint(18733, 20158)
    #     self.client.get(url="/v2/offers/" + str(offerId) + "?excludeRecommend=true",
    #         headers=self.headers)
    #     self.client.close()

    #@task(1)
    #def getOfferByIdRecommend(self):
    #    offerId = randint(18733, 20158)
    #    self.client.get(url="/v2/offers/" + str(offerId) + "/recommend",
    #        headers=self.headers)

    #@task(10)
    #def getFeatureOffers(self):
    #    self.client.get(url="/v2/offers/features?labelId=4&isMatch=true&queryId=60b4534bf2435ac8ab62de50&limit=5",
    #        headers=self.headers)

    # @task(5)
    # def get_banners(self):
    #     self.client.get(
    #         url="/banners",
    #         name="get_banners",
    #         headers=self.headers
    #     )
    #     self.client.close()

    # @task(5)
    # def follow_offers(self):
    #     offer_id = randint(*self.offers_range)
    #     with self.client.post(
    #         url="/offer/follow/" + str(offer_id),
    #         headers=self.headers,
    #         name="follow_offers",
    #         catch_response=True
    #     ) as response:
    #         if response.status_code == 400:
    #             response.success()
    #     self.client.close()

    @task(5)
    def get_follow_offers(self):
        with self.client.get(
            url="/v2/offers/follow",
            headers=self.headers,
            name="get_follow_offers",
            catch_response=True
        ) as response:
            if response.status_code == 400:
                response.success()
        self.client.close()

    # @task(5)
    # def internal_follow_offers(self):
    #     account_id = randint(*self.account_range)
    #     query = {
    #       'page': 0,
    #       'size': 30
    #     }
    #     with self.client.post(
    #         url=f"/internal/offer/follow/{account_id}",
    #         headers=self.headers,
    #         name="internal_follow_offers",
    #         json=query,
    #         catch_response=True
    #     ) as res:
    #       print(res)
    #     self.client.close()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.2)
