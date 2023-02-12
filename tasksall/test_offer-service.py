from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.agents = ['sbconsumeragent/1.0', 'sbandroidagent/1.0', 'sbiosagent/1.0']
        self.mobile_headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
        }
        self.redirectHeaders = {
            'Authorization': 'Bearer eyJpZCI6NDkxOTUyN30=',
            'Content-Type': 'application/json',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0'
        }
        self.redirectBody = {
            'browserName': 'Chrome',
            'browserVersion': '1.0.0',
            'browserPlatform': 'Mac',
            'advertisingId': '78ccb948',
            'referrerUrl': 'store',
            'appsflyerId': '1234',
            'platformTrackingId': '1234'
        }
        # Merchant IDs list get from shopback.sg homepage on 18th Jul 2021
        popularMerchantIds = [
            19354, 18309, 25983,
            19338, 19329, 25569,
            19352, 19307, 19335,
            19160, 18121, 18133]
        dinningMerchantIds = [
            19353, 25811, 18181,
            18897, 18046, 19940,
            18053, 18320, 18170,
            18178, 18947, 18591]
        electronicsMerchantIds = [
            18280, 22885, 19298,
            19333, 18309, 19352,
            19310, 18896, 19785,
            18185, 19082, 18183]
        healthAndBeautyMerchantIds = [
            18335, 19047, 17870,
            17912, 18133, 18796,
            18899, 18046, 18484,
            19336, 18309, 19311,
            17870]
        self.merchantIds = [*popularMerchantIds, *dinningMerchantIds,
                            *electronicsMerchantIds, *healthAndBeautyMerchantIds]
        # Recommended Deals from Reco Engine. Up-to-date on 30th Jul 2021
        self.dealIds = [
            119575, 119122, 118941, 118085,  62560,
            53116, 120443, 117882, 119454, 114044,
            120058, 120066, 119601, 112647,  81892,
            77990,  71544, 112791, 107866,  75943,
            111614,  76571,  58432,  56535,  64043,
            119499, 106597,  76488, 58444,
            47365, 120721,  61662, 120826,  57266,
            118131,  38612, 120939, 120933,  38548,
            1254,  66664,  50933, 120792, 117323]
        # IOS Affiliate Link of Recommended Deals. Up-to-date on 30th Jul 2021
        self.affiliateLinkIds = [
            162333, 266568, 175149, 271683, 276579,
            297855, 183411, 296649, 189585, 281388,
            193239, 193260, 198819, 242934, 202266,
            285444, 246753, 215439, 216129, 216201,
            216333, 296463, 290280, 251046, 302271,
            252429, 303456, 253266, 304062, 259572,
            309995, 311942, 312641, 319835, 321077,
            323111, 323405, 323881, 323995, 327014,
            327053, 328815, 330377, 330757, 330775,
            330885, 331351, 331369, 331773, 332055]

    @task(100)
    def getMerchantDeals(self):
        merchantId = random.choice(self.merchantIds)
        agent = random.choice(self.agents)
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/deals',
            headers= {
                'X-Shopback-Agent': agent
            }
        )

    @task(50)
    def redirectByDealId(self):
        dealId = random.choice(self.dealIds)
        self.client.post(
            url='/v1/deals/' + str(dealId) + '/redirect',
            headers=self.redirectHeaders,
            json=self.redirectBody
        )


    @task(50)
    def redirectByAffiliateLinkId(self):
        affiliateLinkId = random.choice(self.affiliateLinkIds)
        self.client.post(
            url='/v1/deals/' + str(affiliateLinkId) + '/redirect',
            headers=self.redirectHeaders,
            json=self.redirectBody
        )

    @task(7)
    def getMerchantExpiredDeals(self):
        merchantId = random.choice(self.merchantIds)
        agent = random.choice(self.agents)
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/deals/expired',
            headers= {
                'X-Shopback-Agent': agent
            }
        )

    @task(7)
    def getMerchantSimilarDeals(self):
        merchantId = random.choice(self.merchantIds)
        agent = random.choice(self.agents)
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/similar-deals',
            headers= {
                'X-Shopback-Agent': agent
            }
        )

    @task(1)
    def getMobileTopDeals(self):
        self.client.get(
            url='/mobile/top-deals',
            headers=self.mobile_headers
        )

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(1, 10)
