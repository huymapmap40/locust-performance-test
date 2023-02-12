from locust import TaskSet, task, HttpUser, between
import base64
import json
import random
import requests
import copy

myusername = "dev"
mypassword = "iloveshopback14"
# Get this info from mongo mobile-content.component_merchants_reco
mobileContentMerchantsReco = "5ed711653f71e061c57b3646"
# Get this info from mongo mobile-content.compoent
mobileContentComponents = "5d6e6661e2d4137e189ef147"
# Get this info from mongo shopback.pages
shopbackPageId = "5aa0b4ab738a460e0c15d7b1"

DOMAIN = "www.shopback.com.au"
COUNTRY = "AU"
API_GATEWAY = "http://gateway.shopback.com.au"
MERCHANT_PAGE = "ebay-australia"
CAMPAIGN_PAGE = "tech-and-gadgets"
CHALLENGE_ID = "5f8985604fadfc8b81505af0"
STORE_AFFILIATE_ID = "31356"
MERCHANT_ID = 7953
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.com.au',
    'X-Shopback-Build': '2740099',
    'X-Shopback-Agent': 'sbandroidagent/2.74.0',
    'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
    'X-Shopback-Client-User-Agent': 'Locust test',
    'X-Shopback-Language': 'en',
    "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210"
}


def login(email, password):
    url = "{}/members/sign-in".format(API_GATEWAY)
    payload = json.dumps({
        "email": email,
        "password": password,
        "client_user_agent": "test"
    })
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    if response.status_code == 200:
        if 'auth' in response.json():
            return response.json()['auth']['access_token']
    print('Cant to get token {}'.format(response.json()))
    exit(1)


class DeviceUser(HttpUser):
    wait_time = between(3, 5)

    def __init__(self, parent):
        super(DeviceUser, self).__init__(parent)
        self.play_response = {}
        self.counter = 0
        EMAIL="test123@test123.com"
        PASSWORD = mypassword
        jwtToken = login(EMAIL, PASSWORD)
        headers = copy.deepcopy(HEADERS)
        headers['Authorization'] = 'JWT {}'.format(jwtToken)
        self.headers = headers

        self.anomyHeaders = {
            "X-Shopback-Agent": "sbconsumeragent/1.0",
            "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210"
        }

    # GET /mobile-content/v1/components/:id
    @task
    def getMobileContentV1Components(l):
        l.client.get("%s/mobile-content/v1/components/%s?displayType=default&limit=24&offset=0" %
                     (API_GATEWAY, mobileContentComponents), name="/mobile-content/v1/components/:id", headers=l.headers)
#    This endpoint didn't process high volume traffic before 1111 and after 1010 so comment it for 1111 load test
#    # GET /mobile/stores
#    @task
#    def gwMobileStores(l):
#
#        l.client.get("%s/mobile/stores" % API_GATEWAY,
#                     name="/mobile/stores", headers=l.headers)
#    This endpoint didn't process high volume traffic before 1111 and after 1010 so comment it for 1111 load test
#    # GET /mobile/services/configurations
#    @task
#    def gwMobileServiceConfigurations(l):
#        l.client.get("%s/mobile/services/configurations" % API_GATEWAY,
#                     name="/mobile/services/configurations", headers=l.headers)

    # GET /mobile-content/v1/component/merchants-reco/:id
    @task
    def geMobileContentMerchantsReco(l):
        l.client.get("%s/mobile-content/v1/component/merchants-reco/%s?limit=15" % (API_GATEWAY,
                                                                                    mobileContentMerchantsReco), name="/mobile-content/v1/component/merchants-reco/:id", headers=l.headers)

    #GET /cashbacks/latest
    @task
    def gwCashbacksLatest(l):
        l.client.get("%s/cashbacks/latest" % API_GATEWAY,
                     name="/cashbacks/latest", headers=l.headers)

    #GET /mobile/configurations
    @task(2)
    def gwMobileConfiugrations(l):
        l.client.get("%s/mobile/configurations" % API_GATEWAY,
                     name="/mobile/configurations", headers=l.headers)

    #GET /api/v3/stores
    @task
    def gwApiV3Stores(l):
        l.client.get("%s/api/v3/stores" % API_GATEWAY,
                     name="/api/v3/stores", headers=l.headers)

    # GET /int*
    @task
    def gwIntStoreaffiliates(self):
        self.client.get("{}/int/storeaffiliates/{}?account_type=&include=storet".format(API_GATEWAY, STORE_AFFILIATE_ID)
                        , name="/int/storeaffiliates", headers=self.anomyHeaders)

#    This endpoint didn't process high volume traffic before 1111 and after 1010 so comment it for 1111 load test
#    # GET /pages*
#    @task
#    def gwPages(l):
#        l.client.get("{}/pages?slug=%2Fall-stores".format(API_GATEWAY),
#                     name="/pages", headers=l.headers)

    #POST /mobile/devices
    @task
    def gwMobileDevices(l):
        account_ids = ["5158766"]
        account_id = random.choice(account_ids)
        devices = [{'agent': 'sbiosagent/2.66.0-SNAPSHOT',
                    'type': 'iOS', 'model': 'iPhone'}]
        device = random.choice(devices)
        deviceSuffix_list = random.randint(10000, 99999)
        device_id = 'abcde{}'.format(deviceSuffix_list)
        l.headers["X-Device-Id"] = device_id
        l.headers["X-Shopback-Client-User-Agent"] = device_id

        payload = {
            "deviceType": device['type'],
            "accountId": account_id,
            "alertPayment": False,
            "appVersion": "2.70.98",
            "deviceOS": "12.1.2",
            "alertPriceDrop": False,
            "timeZone": "Asia/Taipei",
            "deviceModel": device['model'],
            "deviceId": device_id,
            "alertCashback": False,
            "deviceToken": "3df7dade6a51f4bfc596b1a754c02852342b8b67627eeccfeeb3d2a6a9165d35"
        }
        l.client.post("%s/mobile/devices" % API_GATEWAY,
                      name="/mobile/devices", json=(payload), headers=l.headers)

    # GET Shopback/
    @task
    def sb(l):
        l.client.get("https://%s/" % DOMAIN,
                     name="Shopback /", headers=l.headers)

    # GET Shopback/lazada
    @task
    def sbMerchantPage(l):
        l.client.get("https://%s/%s" % (DOMAIN, MERCHANT_PAGE),
                     name="Shopback /%s" % MERCHANT_PAGE, headers=l.headers)
    # GET /member/v3/me
    @task
    def membersMe(self):
        response = self.client.get(
            url="%s/members/v3/me?type=mobile" % API_GATEWAY, name="/members/v3/me", headers=self.headers)
    @task
    def sbCampaignPage(self):
        self.client.get(url="https://{}/{}".format(DOMAIN, CAMPAIGN_PAGE)
                        , name="Shopback campaign /{}".format(CAMPAIGN_PAGE)
                        , headers=self.headers)

########## Challange service ############

#    @task
#    def challengeHomeList(self):
#
#        self.client.get(
#            url="%s/v2/challenges/limited-time-challenges?offset=0&limit=50&sortBy=rank" % API_GATEWAY,
#            headers=self.headers
#        )
#
#    @task
#    def perkPartnershipMerchantProgram(self):
#
#        self.client.post(
#            url="%s/v2/challenges/partnership-merchant-programs" % API_GATEWAY,
#            headers=self.headers
#        )
#
#    @task
#    def perkMerchantChallenges(self):
#
#        self.client.get(
#            url="%s/v2/challenges/merchant-challenges" % API_GATEWAY,
#            headers=self.headers
#        )
#
#    @task
#    def perkPartnershipChallenge(self):
#
#        self.client.get(
#            url="%s/v2/challenges/partnership-challenges" % API_GATEWAY,
#            headers=self.headers
#        )
#
#    
#
#    # This test will affect data so please consider when run on PROD env
#    # @task
#    def optInChallenge(self):
#
#        self.client.post(
#            url='%s/v2/challenges/limited-time-challenges/%s/opt-in' % (API_GATEWAY,CHALLENGE_ID),
#            headers=self.headers
#        )
#
#    @task
#    def challengePowerscreen(self):
#
#        self.client.get(
#            url='%s/v2/challenges?codes=LOADTEST_1010&customSorts=codes' % API_GATEWAY,
#            headers=self.headers
#        )
#
#    @task
#    def currentChallenge(self):
#
#        response = self.client.get(
#            url='%s/v2/challenges/current-challenges?offset=0&limit=100&sortBy=rank' % API_GATEWAY,
#            headers=self.headers
#        )        
#        # print('Cant to get token {}'.format(response.json()))
#
############ Add after 1111


    @task
    def getMobilePartnerApps(self):

        self.client.get(
            url='%s/mobile/partner-apps' % (API_GATEWAY) ,
            headers=self.headers
        )

    @task
    def getMobileVersions(self):

        self.client.get(
            url='%s/mobile/versions' % (API_GATEWAY) ,
            headers=self.headers
        )

    @task
    def getV1Banners(self):

        self.client.get(
            url='%s/v1/banners' % (API_GATEWAY) ,
            headers=self.headers
        )      

    @task
    def getV1InboxCount(self):

        self.client.get(
            url='%s/v1/inbox/count' % (API_GATEWAY) ,
            headers=self.headers
        )   

    @task
    def getV1Merchants(self):

        self.client.get(
            url='%s/v1/merchants' % (API_GATEWAY) ,
            headers=self.headers
        )           

    @task
    def getV1MerchantById(self):

        self.client.get(
            url='%s/v1/merchants/%s' % (API_GATEWAY,MERCHANT_ID) ,
            headers=self.headers
        )           

    @task
    def getV2MobileServiceConfigurations(self):

        self.client.get(
            url='%s/v2/mobile/services/configurations?build=2890099&platform=Android' % (API_GATEWAY) ,
            headers=self.headers
        )               

    @task
    def getMobileTopDeals(self):

        self.client.get(
            url='%s/mobile/top-deals' % (API_GATEWAY) ,
            headers=self.headers
        )               


    
       