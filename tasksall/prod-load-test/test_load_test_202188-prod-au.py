from locust import TaskSet, task, HttpUser, between
import base64
import json
import random
import requests
import copy

myemail=""
mypassword =""


DOMAIN = "www.shopback.com.au"
COUNTRY = "SG"
API_GATEWAY = "https://sinch.prod-au.svc.shopback.com"
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.com.au',
    'X-Shopback-Build': '3310099',
    'X-Shopback-Agent': 'sbandroidagent/3.31.0',
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
        EMAIL=myemail
        PASSWORD = mypassword
        jwtToken = login(EMAIL, PASSWORD)
        headers = copy.deepcopy(HEADERS)
        headers['Authorization'] = 'JWT {}'.format(jwtToken)
        self.headers = headers

        self.anomyHeaders = {
            "X-Shopback-Agent": "sbconsumeragent/1.0",
            "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210"
        }
    #GET /cashbacks/latest
    @task
    def getCashbacksLatest(l):
        l.client.get("%s/cashbacks/latest" % API_GATEWAY,
                     name="/cashbacks/latest", headers=l.headers)

    # GET /earn-more/v4/challenge-home                     
    @task
    def getEarnMoreV4Challengehome(l):
        l.client.get("%s/earn-more/v4/challenge-home" % API_GATEWAY,
                     name="/earn-more/v4/challenge-home", headers=l.headers)
    
    # GET /ecommerce/mobile/listing-groups/SBV_ShopbackGiftCards
    @task
    def getEcommerceMobileListGroupsSbocZaloraSplws(l):
        l.client.get("%s/ecommerce/mobile/listing-groups/SBV_JBHiFiGiftCards" % API_GATEWAY,
                     name="/ecommerce/mobile/listing-groups/SBV_JBHiFiGiftCards", headers=l.headers)

    # GET /ecommerce/mobile/listing-groups/sboc_ZALORAStoreCredit_30.00_2021-07-08_splws/recommendations
    @task
    def getEcommerceMobileListGroupsSbocZaloraSplwsRecommendations(l):
        l.client.get("%s/ecommerce/mobile/listing-groups/SBOCEcomm_IKEA_20_110521/recommendations" % API_GATEWAY,
                     name="/ecommerce/mobile/listing-groups/SBOCEcomm_IKEA_20_110521/recommendations", headers=l.headers)

    # GET /feature-flag/app-reward/v1/configurations?variationId=60da9440b946c87d9ad1bf3d
    @task
    def getFeatureFlagAppRewardV1Configurations(l):
        l.client.get("%s/feature-flag/app-reward/v1/configurations?variationId=60da99dbb946c87d9ad1bf43" % API_GATEWAY,
                     name="/feature-flag/app-reward/v1/configurations?variationId=60da99dbb946c87d9ad1bf43", headers=l.headers)

    # GET /members/v3/me?type=mobile
    @task
    def getMembersV3Me(l):
        l.client.get("%s/members/v3/me?type=mobile" % API_GATEWAY,
                     name="/members/v3/me?type=mobile", headers=l.headers)
    
    # GET /mobile-content/v1/component/deals-manual/60e815956a46812b06760d24?offset=0&limit=69
    @task
    def getMobileContentV1ComponentDealsManual(l):
        l.client.get("%s/mobile-content/v1/component/deals-manual/60bd9bf616d004300b446f21?offset=0&limit=69" %
                     API_GATEWAY, name="/mobile-content/v1/component/deals-manual/60bd9bf616d004300b446f21?offset=0&limit=69", headers=l.headers)

    # GET /mobile-content/v1/powerscreens/sbocwomensale
    @task
    def getMobileContentV1PowerScreensSbocWomesale(l):
        l.client.get("%s/mobile-content/v1/powerscreens/activationbonus" %
                     API_GATEWAY, name="/mobile-content/v1/powerscreens/activationbonus", headers=l.headers)   

    #GET /mobile/configurations
    @task(2)
    def getMobileConfiugrations(l):
        l.client.get("%s/mobile/configurations" % API_GATEWAY,
                     name="/mobile/configurations", headers=l.headers)

    # GET /orca/favorite/notification/product
    @task
    def getOrcaFavoriteNotificationProduct(l):
        l.client.get("%s/orca/favorite/notification/product" %
                     API_GATEWAY, name="/orca/favorite/notification/product", headers=l.headers)    

    # @task
    # def getOrcaFavoriteProduct(l):
    #     l.client.get("%s/orca/favorite/product?includeGroup=1&page=1&sizePerPage=20" %
    #                  API_GATEWAY, name="/orca/favorite/product?includeGroup=1&page=1&sizePerPage=20", headers=l.headers)    

    

    # POST /plo/appsflyer-data
    @task
    def postPloAppsflyerData(l):
        payload = {
            "appsflyerId":"1627885062516-5743248247694129872",
            "platformTrackingId":"48b9e5cd-8914-4712-928f-e77350a57327",
            "userAgent":"Android"
        }
        
        l.client.post("%s/plo/appsflyer-data" %
                     API_GATEWAY, name="/plo/appsflyer-data",json=(payload),  headers=l.headers)    


    #GET /plo/paymentmethods   
    @task
    def getPloPaymentmethods(l):
        l.client.get("%s/plo/paymentmethods" %
                     API_GATEWAY, name="/plo/paymentmethods", headers=l.headers)    

    #GET /referral/code
    @task
    def getReferralCode(l):
        l.client.get("%s/referral/code" %
                     API_GATEWAY, name="/referral/code", headers=l.headers)    

    #POST /sbgo-deal-service/deals/search  
    @task
    def postSbgoDealServiceDealsSearch(l):
        payload = {
            "calloutType":"socialProofing",
            "limit":6.0,
            "clubbed": True,
            "statuses":["available","scheduled"],
            "location":{
                "lat":-33.873401,
                "lon":151.2031446
            },
            "sort":{"type":"location"},
            "fields":["calloutLabel","location","subtitle"],
            "tags":["sbgo-deal-group-all"]
        }
        
        
        
        l.client.post("%s/sbgo-deal-service/deals/search" %
                     API_GATEWAY, name="/sbgo-deal-service/deals/search",json=(payload),  headers=l.headers)    
    #GET /v1/customer/accounts/self-deletion/request
    @task
    def getCustomerAccountsSelfDeletionRequest(l):
        with l.client.get("%s/v1/customer/accounts/self-deletion/request" %
                     API_GATEWAY, name="/v1/customer/accounts/self-deletion/request", headers=l.headers,catch_response=True)  as response:
              if response.status_code == 404:
                response.success()

    #GET /v1/inbox/count
    @task
    def getV1InbocCount(l):
        l.client.get("%s/v1/inbox/count" %
                     API_GATEWAY, name="/v1/inbox/count", headers=l.headers)    

    #GET /v1/inbox/count
    @task
    def getV1Merchants19354(l):
        l.client.get("%s/v1/merchants/25322" %
                     API_GATEWAY, name="/v1/merchants/25322", headers=l.headers)    

    #GET /v1/merchants/19354/deals
    @task
    def getV1Merchants19354Deals(l):
        l.client.get("%s/v1/merchants/25322/deals" %
                     API_GATEWAY, name="/v1/merchants/25322/deals", headers=l.headers)    

    #POST /v1/merchants/19354/redirect
    @task
    def postV1Merchants19354Redirect(l):
        payload = {
            "appsflyerId": "1597735295542-32314",
            "browser_name": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 shopback-inapp-web-ios",
            "browser_platform": "ios",
            "browser_version": "3.32.1",
            "device_id": "86FA5BE4-D7CE-4BC7-84DF-71088EDA84EE",
            "platformTrackingId": "86FA5BE4-D7CE-4BC7-84DF-71088EDA84EE",
            "redirectData": {},
            "referrer_url": "store",
            "searchKeyword": ""
        }
        
        
        l.client.post("%s/v1/merchants/25322/redirect" %
                     API_GATEWAY, name="/v1/merchants/25322/redirect",json=(payload),  headers=l.headers)    
    
    #GET /v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded
    @task
    def getV1RewardVouchersMyReward(l):
        l.client.get("%s/v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded" %
                     API_GATEWAY, name="/v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded", headers=l.headers)    
    #GET /v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_JUL_SBOC_WOMENSALE_ALL_LUCKYDRAW
    @task
    def getV2Challenges(l):
        l.client.get("%s/v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_JUL_SBOC_WOMENSALE_ALL_LUCKYDRAW" %
                     API_GATEWAY, name="/v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_JUL_SBOC_WOMENSALE_ALL_LUCKYDRAW", headers=l.headers)    
    #GET /v2/challenges/merchant-challenges?limit=1000
    @task
    def getV2ChallengesMerchantChallenges(l):
        l.client.get("%s/v2/challenges/merchant-challenges?limit=1000" %
                     API_GATEWAY, name="/v2/challenges/merchant-challenges?limit=1000", headers=l.headers)    
    
    #GET /v2/challenges/partnership-challenges?limit=1000
    @task
    def getV2ChallengesPartnershipChallenges(l):
        
        l.client.get("%s/v2/challenges/partnership-challenges?limit=1000" %
                     API_GATEWAY, name="/v2/challenges/partnership-challenges?limit=1000", headers=l.headers)    
    
    #POST /v2/challenges/partnership-merchant-programs
    @task
    def postV2ChallengesPartnershipMerchantPrograms(l):
        payload = {"limit":1000}
        l.client.post("%s/v2/challenges/partnership-merchant-programs" %
                     API_GATEWAY, name="/v2/challenges/partnership-merchant-programs",json=(payload), headers=l.headers)    
    
    #GET /v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank
    @task
    def getV2ChallengesUhsChallenges(l):
        l.client.get("%s/v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank" %
                     API_GATEWAY, name="/v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank", headers=l.headers)    
    
    #GET /v2/reward/badges/vouchers-linked
    @task
    def getV2RewardBadgesVouchersLinked(l):
        l.client.get("%s/v2/reward/badges/vouchers-linked" %
                     API_GATEWAY, name="/v2/reward/badges/vouchers-linked", headers=l.headers)    

    #Update after load test on staging-sg

    #GET //categories/level/0?country=SG&fields=name%2Cid%2CisLive%2Cpriority
    @task
    def getCategoriesLevel0(l):
        l.client.get("%s/categories/level/0?country=AU&fields=name,id,isLive,Cpriority"  %
                     API_GATEWAY, name="/categories/level/0?country=AU&fields=name,id,isLive,Cpriority", headers=l.headers)    

    #GET /v2/mobile/services/configurations?build=3320000&platform=Android
    @task
    def getV2MobileServicesConfigurations(l):
        l.client.get("%s/v2/mobile/services/configurations?build=3320000&platform=Android"  %
                     API_GATEWAY, name="/v2/mobile/services/configurations?build=3320000&platform=Android", headers=l.headers)    

    #GET /v1/banners
    @task
    def getV1Banners(l):
        l.client.get("%s/v1/banners"  %
                     API_GATEWAY, name="/v1/banners", headers=l.headers)    

    #GET /v1/merchants?offset=0&limit=12                     
    @task
    def getV1Merchants(l):
        l.client.get("%s/v1/merchants?offset=0&limit=12"  %
                     API_GATEWAY, name="/v1/merchants?offset=0&limit=12", headers=l.headers)    

    #GET /mobile/campaigns
    @task
    def getMobileCampaigns(l):
        l.client.get("%s/mobile/campaigns"  %
                     API_GATEWAY, name="/mobile/campaigns", headers=l.headers)    

    #GET /v1/merchants?offset=0&limit=200
    @task
    def getV1Merchants200(l):
        l.client.get("%s/v1/merchants?offset=0&limit=200"  %
                     API_GATEWAY, name="/v1/merchants?offset=0&limit=200", headers=l.headers)    
    #GET /v1/merchants?offset=200&limit=200
    @task
    def getV1Merchants400(l):
        l.client.get("%s/v1/merchants?offset=200&limit=200"  %
                     API_GATEWAY, name="/v1/merchants?offset=200&limit=200", headers=l.headers)                         

    #GET /v1/merchants?offset=400&limit=200
    @task
    def getV1Merchants600(l):
        l.client.get("%s/v1/merchants?offset=400&limit=200"  %
                     API_GATEWAY, name="/v1/merchants?offset=400&limit=200", headers=l.headers)                         

    #GET /v1/merchants?offset=600&limit=200
    @task
    def getV1Merchants600(l):
        l.client.get("%s/v1/merchants?offset=600&limit=200"  %
                     API_GATEWAY, name="/v1/merchants?offset=600&limit=200", headers=l.headers)                         
    #GET /mobile/versions
    @task
    def getMobileVersions(l):
        l.client.get("%s/mobile/versions"  %
                     API_GATEWAY, name="/mobile/versions", headers=l.headers)                         

    #GET /mobile/partner-apps
    @task
    def getMobilePartnerApps(l):
        l.client.get("%s/mobile/partner-apps"  %
                     API_GATEWAY, name="/mobile/partner-apps", headers=l.headers)                         

    #GET /mobile/services/configurations?build=3320000&platform=Android
    @task
    def getMobileServicesConfigurations(l):
        l.client.get("%s/mobile/services/configurations?build=3320000&platform=Android"  %
                     API_GATEWAY, name="/mobile/services/configurations?build=3320000&platform=Android", headers=l.headers)                         
    #GET /mobile/banners
    @task
    def getMobileBanners(l):
        l.client.get("%s/mobile/banners"  %
                     API_GATEWAY, name="/mobile/banners", headers=l.headers)                         
    #GET /mobile/stores?offset=0&limit=12
    @task
    def getMobileStores(l):
        l.client.get("%s/mobile/stores?offset=0&limit=12"  %
                     API_GATEWAY, name="/mobile/stores?offset=0&limit=12", headers=l.headers)                         
    #GET /v2/mobile/services/configurations
    @task
    def getV2MobileServicesConfigurations(l):
        l.client.get("%s/v2/mobile/services/configurations"  %
                     API_GATEWAY, name="/v2/mobile/services/configurations", headers=l.headers)                         
    
    #GET /plo/mobile/configurations?coordinates=1.2770321,103.8458774
    @task
    def getPloMobileConfigurations(l):
        l.client.get("%s/plo/mobile/configurations?coordinates=-33.873401,151.2031446"  %
                     API_GATEWAY, name="/plo/mobile/configurations?coordinates=-33.873401,151.2031446", headers=l.headers)   