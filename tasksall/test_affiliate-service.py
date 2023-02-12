from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    @task(3)
    def mobileRedirect(self):
        storeAffiliateId = random.choice([66249, 60619, 159324, 66258, 159370, 183673, 60609, 60608, 60611, 60610])
        payload = {
            'browser_name': 'Chrome',
            'browser_version': '1.0.0',
            'browser_platform': 'Mac',
            'referrerUrl': 'store'
        }
        headers = {
            'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
            'Content-Type': 'application/json',
            'X-Shopback-Agent': random.choice(['sbiosagent/1.0', 'sbandroidagent/1.0']),
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.goshopback.vn'
        }

        self.client.post(
            url='/mobile/stores/redirect/' + str(storeAffiliateId),
            headers=headers,
            json=payload
        )

    @task(3)
    def v1WebRedirect(self):
        webAffiliateLinkIds = [159489, 159324, 66258, 159370, 183673, 159481, 159480]
        affiliateLinkId = random.choice(webAffiliateLinkIds)
        headers = {
            'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
            'Content-Type': 'application/json',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.goshopback.vn',
            'X-Shopback-Agent': random.choice(['sbconsumeragent/1.0', 'sbmwebagent/1.0'])
        }
        payload = {
            'browserName': 'Chrome',
            'browserVersion': '1.0.0',
            'browserPlatform': 'Mac',
            'advertisingId': '78ccb948',
            'referrerUrl': 'store'
        }
        self.client.post(
            url='/v1/affiliate-links/' + str(affiliateLinkId) + '/redirect',
            headers=headers,
            json=payload
        )

    @task(3)
    def v1DealRedirect(self):
        webAffiliateLinkIds = [66249, 60619, 159324, 66258, 159370, 183673, 60609, 60608, 60611, 60610]
        affiliateLinkId = random.choice(webAffiliateLinkIds)
        headers = {
            'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
            'Content-Type': 'application/json',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.goshopback.vn',
            'X-Shopback-Agent': random.choice(['sbiosagent/1.0', 'sbandroidagent/1.0'])
        }
        payload = {
            'browserName': 'Chrome',
            'browserVersion': '1.0.0',
            'browserPlatform': 'Mac',
            'advertisingId': '78ccb948',
            'referrerUrl': 'store'
        }
        self.client.post(
            url='/v1/deals/' + str(affiliateLinkId) + '/redirect',
            headers=headers,
            json=payload
        )

    @task(3)
    def v1MerchantRedirect(self):
        merchantIds = [12509, 12727, 19981, 12569, 12501, 12719, 12720]
        merchantId = random.choice(merchantIds)
        headers = {
            'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
            'Content-Type': 'application/json',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.goshopback.vn',
            'X-Shopback-Agent': random.choice(['sbiosagent/1.0', 'sbandroidagent/1.0'])
        }
        payload = {
            'browserName': 'Chrome',
            'browserVersion': '1.0.0',
            'browserPlatform': 'Mac',
            'advertisingId': '78ccb948',
            'referrerUrl': 'store'
        }
        self.client.post(
            url='/v1/merchants/' + str(merchantId) + '/redirect',
            headers=headers,
            json=payload
        )

    @task(1)
    def v1GetAffiliateLink(self):
        affiliateLinkIds =[66249, 60619, 159324, 66258, 159370, 183673, 60609, 60608, 60611, 60610]
        affiliateLinkId = random.choice(affiliateLinkIds)
        self.client.get(
            url='/v1/affiliate-links/' + str(affiliateLinkId),
            headers={'Content-Type': 'application/json'}
        )

    @task(1)
    def v1GetAffiliateLinks(self):
        self.client.get(
            url='/v1/affiliate-links/66249,60619,159324,66258,159370,183673,60609,60608,60611,60610,159489,159324,66258,159370,183673,159481,159480',
            headers={'Content-Type': 'application/json'}
        )



class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0, 1)

