from locust import HttpLocust, TaskSequence, seq_task, TaskSet, task
import base64
import random
import json



storeIds = [4,44,56,64,68,101,103,126,144,170,181,269,276,277,282,322,395,453,498,500,524,536,537,544,548,568,662,680,684]
availablesBuildIds = ["2310291", "231026", "2310295", "2310297", "2310298"]
availableAgents = ['sbandroidagent', 'sbiosagent', 'sbmobileagent']
devices = [
    {
        "agent": "sbandroidagent",
        "buildId": "2310291",
        "deviceId":  "5fe0666ac0329601",
        "deviceToken": "5045f86f9f2c0b0b74b6e64df4b3b3bc5046a2b334c4ad0ed1449b2aea59fd75"
    },
    {
        "agent": "sbiosagent",
        "buildId": "231026",
        "deviceId":  "88b042898ca2bd50",
        "deviceToken": "008347164ba93c9a53660e939051e7c4e8ed97a83eec7dca0ee77d2c8a5ed1be"
    },
    {
        "agent": "sbmobileagent",
        "buildId": "2310295",
        "deviceId":  "4934b05d904bdf25",
        "deviceToken": "2244f830e5206ddf8a4e0546ae21b8a48fc4138ef001583c46dcac6174c86649"
    },
    {
        "agent": "sbiosagent",
        "buildId": "2310295",
        "deviceId":  "e29a37981010560f",
        "deviceToken": "dbe1a4919186a314747c68836d98ec6f72a7b4579adff7974137c617ac178103"
    },
    {
        "agent": "sbmobileagent",
        "buildId": "2310298",
        "deviceId":  "a0f81794d1462a09",
        "deviceToken": "9eae56b7fc8b2168a1cabf58bea8e7f3ac0cd07bdcd8fa72588e4abb92143b89"
    },
    {
        "agent": "sbandroidagent",
        "buildId": "2310298",
        "deviceId":  "e610b2dc596d19fd",
        "deviceToken": "916aef7f0930621a81fe1838e8f643251a0ea2e40ffc6c5ff39bc914c6485945"
    },
]

accounts = []
with open('/scripts/account.json') as json_file:
    jsonData = json.load(json_file)
    accounts = jsonData['accounts']

def genRandomHex(length):
    hex_characters = '0123456789abcdef'
    hex_sample = [random.choice(hex_characters) for _ in range(length)]
    return ''.join(hex_sample)

def cacheHeader():
    ran = random.randint(0, 100)
    cache = 0 if ran < 30 else 1
    mobileCache = "false" if ran < 30 else "true"
    return {
        "X-Response-Cache-Reset": ran, 
        "X-Shopback-No-Cache": mobileCache
    }

def randomItem(items):
    index = random.randint(0, len(items) - 1)
    return items[index]

def getRandomDevice():
    ran = random.randint(0, 100)
    if ran < 30:
        return randomItem(devices)
    else:
        return {
            "agent": randomItem(availableAgents),
            "buildId": randomItem(availablesBuildIds),
            "deviceId":  genRandomHex(16),
            "deviceToken": genRandomHex(64)
        }

## Overview/cashback 166
## Cashback latest 163
## Mobile Store: 132
## Mobile Wordpress: 120
## Mobile PushDevice 93.5
## Mobile TopDeal 72.5
## Mobile\Service\Config 70.8
## MobileBanner 70.2
## Http/ StoreController: 56.4
## storeRedirect 56.4

##1113.6

class UserBehavior(TaskSet):
    def on_start(self):
        self.switchAccount()

    ## Mobile PushDevice 93.5
    @task(9)
    def storePushDevice(self):
        header = self.commonHeader()
        response = self.client.post(
            "/mobile/devices",
            json={
                "alertCashback": "true",
                "accountid": self.accountId,
                "appVersion": self.device["buildId"],
                "deviceType": "iOS" if (self.device["agent"] == "sbiosagent") else "Android",
                "deviceToken": self.device["deviceToken"],
                "alertPayment": "true",
                "deviceModel": "Google Nexus 5 - 4.4.4 - API 19 - 1080x1920",
                "timeZone": "China Standard Time",
                "alertDeals": "true",
                "deviceOS": "4.4.4",
                "deviceId": self.device["deviceId"]
            },
            headers=header
        )

    ## Cashback latest 163
    @task(15)
    def latestCashback(self):
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.get("/cashbacks/latest", headers=header)   

    ## Mobile TopDeal 72.5/2
    @task(4)
    def topDeal(self):
        header = self.commonHeader()
        response = self.client.get("/mobile/top-deals", headers=header)
 
    ## Mobile TopDeal 72.5/2
    @task(3)
    def topDealWithStoreId(self):
        storeId = randomItem(storeIds)
        header = self.commonHeader()
        response = self.client.get("/mobile/top-deals?store_id=%i" % storeId, name="/mobile/top-deals?store_id=[id]", headers=header)


    ## Http/ StoreController: 56.4    
    @task(5)
    def cashbackIndex(self):
        #responseCacheable
        header = self.commonHeader()
        response = self.client.get("/v1/cashbacks?accountUuid=%s" % self.accountUUID, name="/v1/cashbacks?accountUuid=[id]", headers=header)
        

    ## Overview/cashback 166
    @task(14)
    def overviewCashbacks(self):
        #responseCacheable
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.get("/overview/cashbacks", headers=header)
        
    ## Mobile\Service\Config 70.8
    @task(7)
    def serviceConfigurations(self):
        #responseCacheable
        header = self.commonHeader()
        response = self.client.get("/mobile/services/configurations", headers=header)
        
    ## Http/ StoreController: 56.4
    @task(5)
    def storeShow(self):
        #responseCacheable
        storeId = randomItem(storeIds)
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.get("/v3/stores/%i" % storeId,  name="/v3/stores/[id]", headers=header)
        
    ## MobileBanner 70.2
    @task(7)
    def banner(self):
        #responseCacheable
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.get("/mobile/banners", headers=header)
        
  
    ## Mobile Wordpress: 120
    @task(10)
    def wordpressPosts(self):
        #responseCacheable
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.get("/mobile/wordpress-posts", headers=header)
        
    ## storeRedirect 56.4
    @task(11)
    def storeRedirect(self):
        affiliateIds = [9,26,50,55,70,80,87,99,102,130,569,895,997,998,999,1000,1001]
        affiliateId = randomItem(affiliateIds)
        header = { 
            **self.commonHeader(),
            **self.jwtHeader() 
        }
        response = self.client.post(
            "/mobile/stores/redirect/%i" % affiliateId,
            json={
                "browser_name": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel XL Build/OPR3.170623.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
                "browser_version": "1.7.0-SNAPSHOT",
                "browser_platform": "Android",
                "device_id": "a5217aea60017f80",
                "referrer_url": "ride2_aggregation",
                "redirectData": {
                    "pick_up": {
                    "address": "79 Ayer Rajah Crescent, Singapore 139955",
                    "keywords": "79 Ayer Rajah Crescent",
                    "latitude": 1.2980154,
                    "longitude": 103.78744429999999
                    },
                    "drop_off": {
                    "address": "307 Clementi Ave 4, Singapore 120307",
                    "keywords": "307 Clementi Ave 4",
                    "latitude": 1.321453,
                    "longitude": 103.767054
                    },
                    "provider": "grab",
                    "promotion_code": "UOBYOLO",
                    "deeplink": {
                    "productId": 123,
                    "foo": "bar",
                    "taxiTypeId": 69,
                    "vehicleType": "gocar"
                    }
                }
            },
            name="/mobile/stores/redirect/[id]",
            headers=header
        )
        
    ## Mobile Store: 132
    @task(11)
    def storeIndex(self):
        #responseCacheable
        header = self.commonHeader()
        response = self.client.get("/mobile/stores/", headers=header)

    ## pagesShow 56.4
    @task(5)
    def pagesShow(self):
        #responseCacheable
        pageIds = [
            "5d29930a2b106038e54ab4b1",
            "5ca70690fd1154437c260c42",
            "5c94df72c889195f13108a3a",
            "5c8b251639262001f3ae0b6a",
            "5c8242db956e2728780a3893",
            "5c80f9367244036ff14f91d1",
            "5c53d121dd7279068717a0f9",
            "5c51a69b44619a5a6b3c65f1",
            "5c51a5f435043c64dc741531",
            "5c2060ef956e274b942773c1"
        ]
        pageId = randomItem(pageIds)
        header = {
            "X-Shopback-Agent": "sbconsumeragent/1.0",
            "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210",
            "X-Shopback-Language": "en",
            "X-Shopback-Domain": "www.shopback.sg",
            "X-Shopback-Country": "SG",
        }
        response = self.client.get("/int/pages/%s" % pageId,  name="/int/pages/[id]", headers=header)


    def switchAccount(self):
        randomAccount = randomItem(accounts)
        self.accountId = randomAccount["_id"]
        self.accountUUID = randomAccount["uuid"]
        self.device = getRandomDevice()

    def jwtHeader(self):
        tokenObject = {
            "uuid": self.accountUUID,
            "iss":"web",
            "issuedAt":1492088188.859,
            "iat":1492088188,
            "exp":1692089088,
            "id": self.accountId,
        }
        encodedToken = json.JSONEncoder().encode(tokenObject)
        encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
        return {
            "Authorization": 'JWT ' + str(encodedAuth, 'utf-8')
        }
    
    def commonHeader(self):
        return {
            "X-Shopback-Agent": self.device["agent"] + "/1.0",
            "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
            "X-Shopback-Language": "en",
            "X-Shopback-Domain": "www.shopback.sg",
            "X-Shopback-Country": "SG",
            "X-Shopback-Build": self.device["buildId"],
            "Content-Type": "application/json"
        }


class InternalBehavior(TaskSequence):
    @seq_task(1)
    def pagesShow(self):
        #responseCacheable
        pageIds = [
            "5d29930a2b106038e54ab4b1",
            "5ca70690fd1154437c260c42",
            "5c94df72c889195f13108a3a",
            "5c8b251639262001f3ae0b6a",
            "5c8242db956e2728780a3893",
            "5c80f9367244036ff14f91d1",
            "5c53d121dd7279068717a0f9",
            "5c51a69b44619a5a6b3c65f1",
            "5c51a5f435043c64dc741531",
            "5c2060ef956e274b942773c1"
        ]
        pageId = randomItem(pageIds)
        header = {
            "X-Shopback-Agent": "sbconsumeragent/1.0",
            "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210",
            "X-Shopback-Language": "en",
            "X-Shopback-Domain": "www.shopback.sg",
            "X-Shopback-Country": "SG",
        }
        response = self.client.get("/int/pages/%s" % pageId,  name="/int/pages/[id]", headers=header)


class MobileUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 1000

