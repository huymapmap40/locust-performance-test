import json
from random import randint
import urllib.parse
from locust import TaskSet, task, HttpUser, between
import base64
import random
import requests
import copy

myemail="thomas.chuang@shopback.com"
mypassword ="Iloveshopback14"


DOMAIN = "www.shopback.sg"
COUNTRY = "SG"

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.sg',
    'X-Shopback-Build': '3360000',
    'X-Shopback-Agent': 'sbandroidagent/3.36.0-SNAPSHOT',
    'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
    'X-Shopback-Client-User-Agent': 'Locust test',
    'X-Shopback-Language': 'en',
    "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210"
}


def login(self, email, password):
    
    payload = json.dumps({
        "email": email,
        "password": password,
        "client_user_agent": "test"
    })
    response = self.client.post(
        url='/members/sign-in', headers=HEADERS, data=payload)
    
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
        
    def on_start(self):
        jwtToken = login(self, myemail, mypassword)
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
        l.client.get("/cashbacks/latest",
                     name="/cashbacks/latest", headers=l.headers)

   
    @task
    def getEarnMore1(l):
        l.client.get("/earn-more/v5/home-layout",headers=l.headers)
    @task
    def getEarnMore2(l):
        l.client.get("/earn-more/v5/unrevealed-rewards",headers=l.headers)
    @task
    def getEarnMore3(l):
        l.client.get("/earn-more/v5/micro-action-challenges?limit=2",headers=l.headers)
    @task
    def getEarnMore4(l):
        l.client.get("/earn-more/v5/challenge-progress-component?limit=3",headers=l.headers)
    @task
    def getEarnMore5(l):
        l.client.get("/earn-more/v5/discovery-group-challenges/HIGHLIGHTED?limit=6",headers=l.headers)
    @task
    def getEarnMore6(l):
        l.client.get("/earn-more/v5/discovery-group-challenges/P1?limit=6",headers=l.headers)
    @task
    def getEarnMore7(l):
        l.client.get("/earn-more/v5/discovery-group-challenges/P2?limit=6",headers=l.headers)
    @task
    def getEarnMore8(l):
        l.client.get("/earn-more/v5/discovery-group-challenges/SG_1010MONEYHEIST?limit=6",headers=l.headers)
    @task
    def getEarnMore9(l):
        l.client.get("/earn-more/v5/discovery-group-challenges/P3?limit=6",headers=l.headers)

    # GET /ecommerce/mobile/listing-groups/sboc_zalora_splws
    @task
    def getEcommerceMobileListGroupsSbocZaloraSplws(l):
        l.client.get("/ecommerce/mobile/listing-groups/sbgo-go-star-ivegan",
                     name="/ecommerce/mobile/listing-groups/sbgo-go-star-ivegan", headers=l.headers)

    # GET /ecommerce/mobile/listing-groups/sboc_ZALORAStoreCredit_30.00_2021-07-08_splws/recommendations
    @task
    def getEcommerceMobileListGroupsSbocZaloraSplwsRecommendations(l):
        l.client.get("/ecommerce/mobile/listing-groups/SBGOECOMMCVCRAVE1/recommendations",
                     name="/ecommerce/mobile/listing-groups/SBGOECOMMCVCRAVE1/recommendations", headers=l.headers)

    # GET /feature-flag/app-reward/v1/configurations?variationId=60da9440b946c87d9ad1bf3d
    @task
    def getFeatureFlagAppRewardV1Configurations(l):
        l.client.get("/feature-flag/app-reward/v1/configurations?variationId=614a90b0e3770c04e2c6c024",
                     name="/feature-flag/app-reward/v1/configurations?variationId=614a90b0e3770c04e2c6c024", headers=l.headers)

    # GET /members/v3/me?type=mobile
    @task
    def getMembersV3Me(l):
        l.client.get("/members/v3/me?type=mobile",
                     name="/members/v3/me?type=mobile", headers=l.headers)
    
    # GET /mobile-content/v1/component/deals-manual/60e815956a46812b06760d24?offset=0&limit=69
    @task
    def getMobileContentV1ComponentDealsManual(l):
        l.client.get("/mobile-content/v1/component/deals-manual/5fd31f7981ba276f121c3ff2?offset=0&limit=8" , name="/mobile-content/v1/component/deals-manual/5fd31f7981ba276f121c3ff2?offset=0&limit=69", headers=l.headers)

    # GET /mobile-content/v1/powerscreens/sbocwomensale
    @task
    def getMobileContentV1PowerScreensSbocWomesale(l):
        l.client.get("/mobile-content/v1/powerscreens/1111", name="/mobile-content/v1/powerscreens/1111", headers=l.headers)   

    #GET /mobile/configurations
    @task(2)
    def getMobileConfiugrations(l):
        l.client.get("/mobile/configurations",
                     name="/mobile/configurations", headers=l.headers)

    # GET /orca/favorite/notification/product
    # @task
    # def getOrcaFavoriteNotificationProduct(l):
    #     l.client.get("/orca/favorite/notification/product" , name="/orca/favorite/notification/product", headers=l.headers)    

    # @task
    # def getOrcaFavoriteProduct(l):
    #     l.client.get("/orca/favorite/product?includeGroup=1&page=1&sizePerPage=20", name="/orca/favorite/product?includeGroup=1&page=1&sizePerPage=20", headers=l.headers)    

    

    # POST /plo/appsflyer-data
    @task
    def postPloAppsflyerData(l):
        payload = {"appsflyerId":"1635783673119-6779738144370459815","platformTrackingId":"404f5f99-cb8b-4180-86c6-248aa2e8db72","userAgent":"Android"}        
        l.client.post("/plo/appsflyer-data", name="/plo/appsflyer-data",json=(payload),  headers=l.headers)    


    #GET /plo/paymentmethods   
    @task
    def getPloPaymentmethods(l):
        l.client.get("/plo/paymentmethods", name="/plo/paymentmethods", headers=l.headers)    

    #GET /referral/code
    @task
    def getReferralCode(l):
        l.client.get("/referral/code" , name="/referral/code", headers=l.headers)    

    #POST /sbgo-deal-service/deals/search  
    @task
    def postSbgoDealServiceDealsSearch(l):
        payload = {
            "calloutType":"socialProofing",
            "limit":6.0,
            "clubbed":True,
            "statuses":["available","scheduled"],
            "location":{"lat":1.2770321,"lon":103.8458774},
            "sort":{"type":"location"},
            "fields":["calloutLabel","location","subtitle","title","description","value"],
            "tags":["sbgo-deal-group-all"]
        }
        
        
        
        l.client.post("/sbgo-deal-service/deals/search" , name="/sbgo-deal-service/deals/search",json=(payload),  headers=l.headers)    
    #GET /v1/customer/accounts/self-deletion/request
    @task
    def getCustomerAccountsSelfDeletionRequest(l):
        with l.client.get("/v1/customer/accounts/self-deletion/request", name="/v1/customer/accounts/self-deletion/request", headers=l.headers,catch_response=True)  as response:
              if response.status_code == 404:
                response.success()

    #GET /v1/inbox/count
    @task
    def getV1InbocCount(l):
        l.client.get("/v1/inbox/count", name="/v1/inbox/count", headers=l.headers)    

    #GET /v1/inbox/count
    @task
    def getV1Merchants19354(l):
        l.client.get("/v1/merchants/19160", name="/v1/merchants/19160", headers=l.headers)    

    #GET /v1/merchants/19354/deals
    @task
    def getV1Merchants19354Deals(l):
        l.client.get("/v1/merchants/19160/deals", name="/v1/merchants/19160/deals", headers=l.headers)    

    #POST /v1/merchants/19354/redirect
    # no need to run redirect
    # @task
    # def postV1Merchants19354Redirect(l):
    #     payload = {
    #         "appsflyerId": "1597735295542-32314",
    #         "browser_name": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 shopback-inapp-web-ios",
    #         "browser_platform": "ios",
    #         "browser_version": "3.36.0",
    #         "device_id": "86FA5BE4-D7CE-4BC7-84DF-71088EDA84EE",
    #         "platformTrackingId": "86FA5BE4-D7CE-4BC7-84DF-71088EDA84EE",
    #         "redirectData": {},
    #         "referrer_url": "store",
    #         "searchKeyword": ""
    #     }

        
        
    #     l.client.post("/v1/merchants/18699/redirect" , name="/v1/merchants/18699/redirect",json=(payload),  headers=l.headers)    
    
    #GET /v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded
    @task
    def getV1RewardVouchersMyReward(l):
        l.client.get("/v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded" , name="/v1/reward/vouchers/my-reward?offset=0&limit=20&sort=recentlyAdded", headers=l.headers)    

    @task
    def getV2Challenges1(l):
        l.client.get("/v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_2021-11_SBOC_TACTICAL_1111_CODE1_SB_0_0_0_HEIST%2CSG_2021-11_SBOC_TACTICAL_1111_CODE2_SB_0_0_0_HEIST%2CSG_2021-11_SBOC_TACTICAL_1111_CODE3_SB_0_0_0_HEIST" ,name="/v2/challenges", headers=l.headers)   

    @task
    def getV2Challenges2(l):
        l.client.get("/v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_2021-11_SBOC_TACTICAL_0_0_SB_0_0_0_1111MAGIC%2CSG_2021-11_SBOC_TACTICAL_0_0_SB_0_0_0_1111LUNCH%2CSG_2021-11_SBOC_TACTICAL_0_0_SB_0_0_0_1111CLOSING" ,name="/v2/challenges", headers=l.headers)   
    
    @task
    def getV2Challenges3(l):
        l.client.get("/v2/challenges?customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED&codes=SG_2021-10_SBOC_TACTICAL_0_100_MC_0_0_0_LOOKFANTASTIC%2CSG_2021-10_SBOC_FTM_0_100_MC_0_0_0_CIRCLES%2CSG_2021-11_SBOC_FTM_0_100_MC_0_0_0_NORTON%2CSG_2021-10_SBOC_FTM_0_2_MC_0_0_0_IRVIN%2CSG_2021-10_SBOC_FTM_0_15_MC_0_0_0_BRANDS%2CSG_2021-11_SBOC_REACTIVATION_0_100_MC_0_0_0_SEPHORA%2CSG_2021-11_SBOC_FTM_0_100_MC_0_0_0_SEPHORA%2CSG_2021-11_SBOC_FTM_0_10_MC_0_0_0_CIRCLESLIFE%2CSG_2021-11_SBOC_FTM_0_2_MC_0_0_0_SURVEY",name="/v2/challenges", headers=l.headers)  
    #GET /v2/challenges/merchant-challenges?limit=1000
    @task
    def getV2ChallengesMerchantChallenges(l):
        l.client.get("/v2/challenges/merchant-challenges?limit=1000" , name="/v2/challenges/merchant-challenges?limit=1000", headers=l.headers)    
    
    #GET /v2/challenges/partnership-challenges?limit=1000
    @task
    def getV2ChallengesPartnershipChallenges(l):
        
        l.client.get("/v2/challenges/partnership-challenges?limit=1000" , name="/v2/challenges/partnership-challenges?limit=1000", headers=l.headers)    
    
    
    #POST /v2/challenges/partnership-merchant-programs
    @task
    def postV2ChallengesPartnershipMerchantPrograms(l):
        payload = {"limit":1000}
        l.client.post("/v2/challenges/partnership-merchant-programs" , name="/v2/challenges/partnership-merchant-programs",json=(payload), headers=l.headers)    
    
    #GET /v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank
    @task
    def getV2ChallengesUhsChallenges(l):
        l.client.get("/v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank" , name="/v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank", headers=l.headers)    

    #GET /v2/reward/badges/vouchers-linked
    @task
    def getV2RewardBadgesVouchersLinked(l):
        l.client.get("/v2/reward/badges/vouchers-linked" , name="/v2/reward/badges/vouchers-linked", headers=l.headers)    

    #Update after load test on staging-sg

    #GET //categories/level/0?country=SG&fields=name%2Cid%2CisLive%2Cpriority
    @task
    def getCategoriesLevel0(l):
        l.client.get("/categories/level/0?country=SG&fields=name,id,isLive,Cpriority"  , name="/categories/level/0?country=SG&fields=name,id,isLive,Cpriority", headers=l.headers)    

    #GET /v2/mobile/services/configurations?build=3320000&platform=Android
    @task
    def getV2MobileServicesConfigurations(l):
        l.client.get("/v2/mobile/services/configurations?build=3450000&platform=Android" , name="/v2/mobile/services/configurations?build=3360000&platform=Android", headers=l.headers)    

    #GET /v1/banners
    @task
    def getV1Banners(l):
        l.client.get("/v1/banners" , name="/v1/banners", headers=l.headers)    

    #GET /v1/merchants?offset=0&limit=12                     
    @task
    def getV1Merchants(l):
        l.client.get("/v1/merchants?offset=0&limit=12"  , name="/v1/merchants?offset=0&limit=12", headers=l.headers)    

    @task
    def getMobileContentComponentMerchantsAuto1(l):
        l.client.get("/mobile-content/v1/component/merchants-auto/617f538650a3625277c03367?limit=3", headers=l.headers)    
    @task
    def getMobileContentComponentMerchantsAuto2(l):
        l.client.get("/mobile-content/v1/component/merchants-auto/617f53c8e4d24e8c5ced657b?limit=3", headers=l.headers)    
    @task
    def getMobileContentComponentMerchantsAuto3(l):
        l.client.get("/mobile-content/v1/component/merchants-auto/617f5368a6690819ef3e38de?limit=3", headers=l.headers)    
    @task
    def getMobileContentComponentMerchantsAuto4(l):
        l.client.get("/mobile-content/v1/component/merchants-auto/617e545e8449aaa6b4849922?limit=100", headers=l.headers)    

    #GET /mobile/campaigns
    @task
    def getMobileCampaigns(l):
        l.client.get("/mobile/campaigns"  , name="/mobile/campaigns", headers=l.headers)    

    #GET /v1/merchants?offset=0&limit=200
    @task
    def getV1Merchants200(l):
        l.client.get("/v1/merchants?offset=0&limit=200"  , name="/v1/merchants?offset=0&limit=200", headers=l.headers)    
    #GET /v1/merchants?offset=200&limit=200
    @task
    def getV1Merchants400(l):
        l.client.get("/v1/merchants?offset=200&limit=200" , name="/v1/merchants?offset=200&limit=200", headers=l.headers)                         

    #GET /v1/merchants?offset=400&limit=200
    @task
    def getV1Merchants600(l):
        l.client.get("/v1/merchants?offset=400&limit=200" , name="/v1/merchants?offset=400&limit=200", headers=l.headers)                         

    #GET /v1/merchants?offset=600&limit=200
    @task
    def getV1Merchants600(l):
        l.client.get("/v1/merchants?offset=600&limit=200"  , name="/v1/merchants?offset=600&limit=200", headers=l.headers)                         
    #GET /mobile/versions
    @task
    def getMobileVersions(l):
        l.client.get("/mobile/versions"  , name="/mobile/versions", headers=l.headers)                         

    #GET /mobile/partner-apps
    @task
    def getMobilePartnerApps(l):
        l.client.get("/mobile/partner-apps"  , name="/mobile/partner-apps", headers=l.headers)                         

    #GET /mobile/services/configurations?build=3320000&platform=Android
    @task
    def getMobileServicesConfigurations(l):
        l.client.get("/mobile/services/configurations?build=3320000&platform=Android"  , name="/mobile/services/configurations?build=3320000&platform=Android", headers=l.headers)                         
    #GET /mobile/banners
    @task
    def getMobileBanners(l):
        l.client.get("/mobile/banners"  , name="/mobile/banners", headers=l.headers)                         
    #GET /mobile/stores?offset=0&limit=12
    @task
    def getMobileStores(l):
        l.client.get("/mobile/stores?offset=0&limit=12" , name="/mobile/stores?offset=0&limit=12", headers=l.headers)                         
    #GET /v2/mobile/services/configurations
    @task
    def getV2MobileServicesConfigurations(l):
        l.client.get("/v2/mobile/services/configurations"  , name="/v2/mobile/services/configurations", headers=l.headers)                         
    
    #GET /plo/mobile/configurations?coordinates=1.2770321,103.8458774
    @task
    def getPloMobileConfigurations(l):
        l.client.get("/plo/mobile/configurations?coordinates=1.2770321,103.8458774" , name="/plo/mobile/configurations?coordinates=1.2770321,103.8458774", headers=l.headers)   
    
    #Add for 99 load test
    
    # https://api-app.shopback.sg/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP
    @task
    def getEcommerceMobileListsSbgoGongcha(l):
        l.client.get("/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP" , name="/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP", headers=l.headers)   
    #https://api-app.shopback.sg/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/related    
    @task
    def getEcommerceMobileListsSbgoGongchaRelated(l):    
        l.client.get("/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/related" , name="/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/related", headers=l.headers)   

    #https://api-app.shopback.sg/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/locations?lat=1.2770321&lon=103.8458774&limit=1
    @task
    def getEcommerceMobileListsSbgoGongchaLocations(l):    
        l.client.get("/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/locations?lat=1.2770321&lon=103.8458774&limit=1" , name="/ecommerce/mobile/listings/sbgo_GongCha_4.90_a012x00000JMVWrAAP/locations?lat=1.2770321&lon=103.8458774&limit=1", headers=l.headers)           

    #/ecommerce/mobile/listing-groups/SBOCEcomm_Shopee_BAU
    @task
    def getEcommerceMobileListShopee(l):    
        l.client.get("/ecommerce/mobile/listing-groups/SBOCEcomm_Zalora_BAU" , name="/ecommerce/mobile/listing-groups/SBOCEcomm_Zalora_BAU", headers=l.headers)           

    #/ecommerce/mobile/listing-groups/sboc_ShopeeVouchers_5.00_2021-08-10_bau/recommendations
    @task
    def getEcommerceMobileListShopeeRecommendations(l):    
        l.client.get("/ecommerce/mobile/listing-groups/sboc_ZALORAStoreCredit_30.00_2021-10-01_bauQ4/recommendations" , name="/ecommerce/mobile/listing-groups/sboc_ZALORAStoreCredit_30.00_2021-10-01_bauQ4/recommendations", headers=l.headers)           


