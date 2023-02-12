from locust import HttpUser, TaskSet, task
import random
import json


class MobileUserBehavior(TaskSet):
    def __init__(self, parent):
        super(MobileUserBehavior, self).__init__(parent)
        self.mobile_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/2.8.0',
            'Authorization': 'Bearer eyJpZCI6IDQ2ODg0NTN9',
            'X-Request-ID': 'f022449e-b9dd-4485-8e4d-7b6aa5e5a871',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
        }
        self.web_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0.0',
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
            headers=self.mobile_headers
        )
        self.merchants = json.loads(merchantsResponse.text)
        self.merchant = random.choice(self.merchants.get('data'))
        self.storeAffiliateIds = [64765, 83677, 187689, 187690, 187691, 251343, 251344, 251345,
                                  56689, 56820,  62394,  62395,  62396,  62397,  62398,  63238,
                                  64813, 64814,  64815,  64816,  64817,  64818,  68809,  70539,
                                  70780, 70781,  71218,  71219,  71590,  72928,  73195,  73823,
                                  74522, 74523,  74542,  74595,  74852,  75299,  76020,  76493,
                                  76533, 76534,  76583,  76584,  76585,  76689,  76968,  76998,
                                  76999, 77001,  77002,  77202,  77273,  77274,  77586,  77660,
                                  78986, 79565,  79755,  79756,  80054,  80856,  80857,  80858,
                                  80859, 80860,  80861,  80862,  80863,  80864,  80865,  80866,
                                  80867, 80868,  80869,  80870,  81088,  81251,  81581,  81582,
                                  81583, 81584,  81585,  81586,  81587,  81588,  81589,  81590,
                                  81591, 81592,  81593,  81594,  81595,  81596,  81597,  81598,
                                  81599, 81600,  82307,  82308]
        self.storeAffiliateId = random.choice(self.storeAffiliateIds)

    @task
    def accessHomescreen(self):
        self.client.get(
            url='/v1/merchants',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/mobile/partner-apps',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/categories/level/0',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/banners',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants',
            headers=self.mobile_headers
        )
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/internal/merchants/' + str(merchantId),
            headers=self.mobile_headers
        )

    @task
    def redirectMerchant(self):
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.mobile_headers
        )
        self.client.post(
            url='/v1/merchants/' + str(merchantId) + '/redirect',
            headers=self.mobile_headers)
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/platform-settings',
            headers=self.mobile_headers
        )

    @task
    def redirectDeal(self):
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.mobile_headers
        )
        self.client.post(
            url='/v1/deals/' + str(self.storeAffiliateId) + '/redirect',
            headers=self.mobile_headers)
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/platform-settings',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=DESKTOP_WEB',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=MOBILE_WEB',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=ANDROID_APP',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=IOS_APP',
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=EXTENSION',
            headers=self.mobile_headers
        )

    @task
    def redirectMerchantSearch(self):
        merchantId = self.merchant.get('id')
        merchantName = self.merchant.get('name')
        self.client.get(
            url='/v1/merchants/search?q=' + merchantName,
            headers=self.mobile_headers
        )
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.mobile_headers
        )
        self.client.post(
            url='/v1/merchants/' + str(merchantId) + '/redirect',
            headers=self.mobile_headers)
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/platform-settings',
            headers=self.mobile_headers
        )


class WebUserBehavior(TaskSet):
    def __init__(self, parent):
        super(MobileUserBehavior, self).__init__(parent)
        self.mobile_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/2.8.0',
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
            << << << < HEAD
            headers=self.mobile_headers
        )
        self.merchants = json.loads(merchantsResponse.text)
        self.merchant = random.choice(self.merchants.get('data'))
        self.storeAffiliateIds = [64765, 83677, 187689, 187690, 187691, 251343, 251344, 251345,
                                  56689, 56820,  62394,  62395,  62396,  62397,  62398,  63238,
                                  64813, 64814,  64815,  64816,  64817,  64818,  68809,  70539,
                                  70780, 70781,  71218,  71219,  71590,  72928,  73195,  73823,
                                  74522, 74523,  74542,  74595,  74852,  75299,  76020,  76493,
                                  76533, 76534,  76583,  76584,  76585,  76689,  76968,  76998,
                                  76999, 77001,  77002,  77202,  77273,  77274,  77586,  77660,
                                  78986, 79565,  79755,  79756,  80054,  80856,  80857,  80858,
                                  80859, 80860,  80861,  80862,  80863,  80864,  80865,  80866,
                                  80867, 80868,  80869,  80870,  81088,  81251,  81581,  81582,
                                  81583, 81584,  81585,  81586,  81587,  81588,  81589,  81590,
                                  81591, 81592,  81593,  81594,  81595,  81596,  81597,  81598,
                                  81599, 81600,  82307,  82308]
        self.storeAffiliateId = random.choice(self.storeAffiliateIds)

    @task
    def accessHomepage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs/' + slug,
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.web_headers
        )
        self.client.get(
            url='/categories/level/0',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.mobile_headers
        )

    @task
    def merchantAllPage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs/all-stores',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.mobile_headers
        )

    @task
    def merchantSearchPage(self):
        merchantName = self.merchant.get('name')
        self.client.get(
            url='/v1/merchants/search?q=' + merchantName,
            == == == =
            >>>>>> > master
            headers=self.mobile_headers
        )
        self.merchants = json.loads(merchantsResponse.text)
        self.merchant = random.choice(self.merchants.get('data'))
        self.storeAffiliateIds = [64765, 83677, 187689, 187690, 187691, 251343, 251344, 251345,
                                  56689, 56820,  62394,  62395,  62396,  62397,  62398,  63238,
                                  64813, 64814,  64815,  64816,  64817,  64818,  68809,  70539,
                                  70780, 70781,  71218,  71219,  71590,  72928,  73195,  73823,
                                  74522, 74523,  74542,  74595,  74852,  75299,  76020,  76493,
                                  76533, 76534,  76583,  76584,  76585,  76689,  76968,  76998,
                                  76999, 77001,  77002,  77202,  77273,  77274,  77586,  77660,
                                  78986, 79565,  79755,  79756,  80054,  80856,  80857,  80858,
                                  80859, 80860,  80861,  80862,  80863,  80864,  80865,  80866,
                                  80867, 80868,  80869,  80870,  81088,  81251,  81581,  81582,
                                  81583, 81584,  81585,  81586,  81587,  81588,  81589,  81590,
                                  81591, 81592,  81593,  81594,  81595,  81596,  81597,  81598,
                                  81599, 81600,  82307,  82308]
        self.storeAffiliateId = random.choice(self.storeAffiliateIds)

    @task
    def accessHomepage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs/' + slug,
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.web_headers
        )
        self.client.get(
            url='/categories/level/0',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.web_headers
        )

    @task
    def merchantAllPage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs/all-stores',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/public',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.web_headers
        )

    @task
    def merchantSearchPage(self):
        merchantName = self.merchant.get('name')
        self.client.get(
            url='/v1/merchants/search?q=' + merchantName,
            headers=self.web_headers
        )

    @task
    def merchantPage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs' + slug,
            headers=self.web_headers
        )

        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=DESKTOP_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=MOBILE_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=ANDROID_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=IOS_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=EXTENSION',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.web_headers
        )

    @task
    def redirectDeal(self):
        merchantId = self.merchant.get('id')
        data = {
            "accountId": 4688453,
            "merchantId": merchantId,
            "storeaffiliateId": self.storeAffiliateId,
            "browserName": "Test",
            "browserVersion": "1",
            "browserPlatform": "Test platform"
        }
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/deals/' + str(self.storeAffiliateId),
            headers=self.web_headers)
        self.client.post(
            url='/v1/deals/' + str(self.storeAffiliateId) + '/redirect',
            data=data,
            headers=self.web_headers)
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/affiliate-link',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=DESKTOP_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=MOBILE_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=ANDROID_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=IOS_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=EXTENSION',
            headers=self.web_headers
        )

    @task
    def merchantPage(self):
        slug = self.merchant.get('shortname')
        merchantId = self.merchant.get('id')
        self.client.get(
            url='/v1/slugs' + slug,
            headers=self.web_headers
        )

        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=DESKTOP_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=MOBILE_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=ANDROID_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=IOS_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=EXTENSION',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/merchants/upsize',
            headers=self.web_headers
        )

    @task
    def redirectDeal(self):
        merchantId = self.merchant.get('id')
        data = {
            "accountId": 4688453,
            "merchantId": merchantId,
            "storeaffiliateId": self.storeAffiliateId,
            "browserName": "Test",
            "browserVersion": "1",
            "browserPlatform": "Test platform"
        }
        self.client.get(
            url='/v1/merchants/' + str(merchantId),
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/deals/' + str(self.storeAffiliateId),
            headers=self.web_headers)
        self.client.post(
            url='/v1/deals/' + str(self.storeAffiliateId) + '/redirect',
            data=data,
            headers=self.web_headers)
        self.client.get(
            url='/v1/merchants/' + str(merchantId) + '/affiliate-link',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=DESKTOP_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=MOBILE_WEB',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=ANDROID_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=IOS_APP',
            headers=self.web_headers
        )
        self.client.get(
            url='/v1/internal/merchants/' +
                str(merchantId) + '/e-outlets?platform=EXTENSION',
            headers=self.web_headers
        )


class User(HttpUser):
    tasks = [MobileUserBehavior, WebUserBehavior]
    min_wait = 1000
    max_wait = 1000
