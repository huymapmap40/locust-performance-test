from locust import HttpUser, TaskSequence, seq_task, TaskSet, task
import base64
import random
import json

#Test data
env = {
    "domain" : "www.shopback.com.au",
    "sid" : "AU"
}
storeIds = [473,747,654,525,582,1,820,573,461,450,543,64,327,312,326,711,651,644,501,775,494,836,831,601,526,614,634,506,714,519,524,457,871,790,677,631,340,509,341,664,444,617,452,454,818,702,877,496,336,848]
webStoreIds = [473, 747, 654, 525, 582, 1, 820, 573, 461, 450, 543, 64, 327, 312, 711, 651, 644, 501, 775, 494, 836, 831, 601, 526, 614, 634, 506, 714, 519, 524, 457, 871, 790, 677, 631, 340, 509, 341, 664, 444, 617, 452, 454, 818, 702, 877, 496, 336, 848, 900]
devices = [
    {
        "agent": "sbandroidagent",
        "buildId": "2310298",
        "deviceId":  "5fe0666ac0329601",
        "deviceToken": "5045f86f9f2c0b0b74b6e64df4b3b3bc5046a2b334c4ad0ed1449b2aea59fd75"
    },
    {
        "agent": "sbiosagent",
        "buildId": "2330001",
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
        "buildId": "2330001",
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
availablesBuildIdsForAndroid = [ "2330000", "2330000", "2330001"]
availablesBuildIdForIOS = ["2310291", "231026", "2310295", "2310297", "2310298"]
availableAgents = ['sbandroidagent', 'sbiosagent', 'sbmobileagent']
accounts = []
accountsJson = {
    "accounts":[
        # Adding account for testing here
        {
            "_id" : 731150, #kyle.le@shopback.com
            "uuid" : "4150e5a4c249467cbcbbea2ec5a39142"
        },
        {
            "_id" : 313134, #me@bryanchua.com
            "uuid" : "0c4fbbc97da24b52a81ffe0da4c86acf"
        }
    ]
}
accounts = accountsJson['accounts']

#Generic Function
def genRandomHex(length):
    hex_characters = '0123456789abcdef'
    hex_sample = [random.choice(hex_characters) for _ in range(length)]
    return ''.join(hex_sample)

def randomItem(items):
    index = random.randint(0, len(items) - 1)
    return items[index]

def getEnv():
    return env

def getRandomDevice():
    ran = random.randint(0, 100)
    if ran < 50:
        return randomItem(devices)
    agent = randomItem(availableAgents)
    buildId = randomItem(availablesBuildIdForIOS) if (agent == "sbiosagent") else randomItem(availablesBuildIdsForAndroid)
    return {
        "agent": agent,
        "buildId": buildId,
        "deviceId":  genRandomHex(16),
        "deviceToken": genRandomHex(64)
    }

def jwtHeader(behavior):
    if behavior.accountId == 731150:
        encodedAuth = "ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFkV2xrSWpvaU5ERTFNR1UxWVRSak1qUTVORFkzWTJKalltSmxZVEpsWXpWaE16a3hORElpTENKcGMzTWlPaUozZDNjdWMyaHZjR0poWTJzdVkyOXRJaXdpYVhOemRXVmtRWFFpT2pFMU5qa3dPREV4TURrdU16UXhMQ0pwWVhRaU9qRTFOamt3T0RFeE1Ea3NJbVY0Y0NJNk1UVTNNVFkzTXpFd09YMC5tX0p2MHdQdGJDZm13QlBnbTJELXhENTh4VW9QRjFOdGZnSXhjNzJ0a1czQTRUX0pCaExZZ0RXRWlLN2ZwcC1Qc1ZtbFkwNklEMG5ab3Q2UmlQc3ZLNHRCNVVweXdId3FZN2Y3RUZkV1l3dEZYb3R0RFZUNnNQeGc2cU9DcDhfeDBYQ2MyR1FabmQ2Z3g2X25NUm1TUWNLX29penc4VVdvTXV0Tjh0MWxIMUxtNEQyWnRNQXZHZzFReTVZSWE1NTQzNDZVY19VdzVNc2R3aXUtUXprYmZSdERJSGZHRlBHWU9RRVlpOUhIYW9rOW9PcWdqR0dmTnozV2RYRGZWNmNlMXFxY2ZjcUw2YU81YnlHSWZtR1MyV3Q4NUFld2dFWmx2V3oweHpibzNMLW1uXzY5ZlZfel9GYnJDa1E1S200T09nOFNFQURYVGdZLTBkdEpYZW9fN3c="
    if behavior.accountId == 313134:
        encodedAuth = "ZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFkV2xrSWpvaU1HTTBabUppWXprM1pHRXlOR0kxTW1FNE1XWm1aVEJrWVRSak9EWmhZMllpTENKcGMzTWlPaUozZDNjdWMyaHZjR0poWTJzdVkyOXRJaXdpYVhOemRXVmtRWFFpT2pFMU5qa3dPREV3T1RRdU5UZzFMQ0pwWVhRaU9qRTFOamt3T0RFd09UUXNJbVY0Y0NJNk1UVTNNVFkzTXpBNU5IMC5YalVDMW5CdGRMWHpaUnZpUHJ1ZU84N2ZEVTQ5eFZ1OTNSMHZxX2JWdmJmWGJVcUc0cU1RNTBGVjJOQThuNnpsWnZFdjVlUWtESVdyejBGNHVCam50QUV4TUxsOWMwUllnSG45LVRHMDVySVA1TUJ5X2szNjh6UkNtNWNHc1Q2bmkxYlRZSEd3dlJNY2Z1ZWxoc1BVNjZJZDZMd3U1eDEzT2VZaUo0cFh4UGQwbkI0N1Y5SVdsYlV4S0lhdkc2LS05c1cwUWlpYjNHUGp3V091QjlFYVdWNERTRVprZTVsN1k3ZnhIcTl1M3o1a3RUMEd1YXJoeUdYdjFWRGdHaHR0M0hwUko3WmZDOThmN1ZiSjlFODN1d2R4TjlKZjZhNjFsV0E3VXphR0oxd044YWZ4TlNUT1ZYTDJwLVd4X2xsdXphaFNpM2FxSFZNb1dWSldaemlUb3c="
    return {
        "Authorization": 'JWT ' + encodedAuth
    }
    tokenObject = {
        "uuid": behavior.accountUUID,
        "iss":"web",
        "issuedAt":1492088188.859,
        "iat":1492088188,
        "exp":1692089088,
        "id": behavior.accountId,
    }
    encodedToken = json.JSONEncoder().encode(tokenObject)
    encodedAuth = base64.b64encode(encodedToken.encode("utf-8"))
    return {
        "Authorization": 'JWT ' + str(encodedAuth, 'utf-8')
    }

def commonHeader(behavior):
    return {
        "X-Shopback-Agent": behavior.device["agent"] + "/1.0",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Language": "en",
        "X-Shopback-Domain": env['domain'],
        "X-Shopback-Country": env['sid'],
        "X-Shopback-Build": behavior.device["buildId"],
        "Content-Type": "application/json"
    }

def webHeader(behavior):
    return {
        "X-Shopback-Agent": "sbconsumeragent/1.0",
        "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210",
        "X-Shopback-Language": "en",
        "X-Shopback-Domain": env['domain'],
        "X-Shopback-Country": env['sid'],
    }

# Behaviors
class WebBehavior(TaskSequence):

    def on_start(self):
        self.switchAccount()

    @seq_task(1)
    def pagesShow(self):
        self.switchAccount()
        pageIds = [
            "5d5645641d9f714dfc2f6201",
            "5ae075445f148c3c8547e382",
            "5aa0b4345f148c5c9a650f01",
            "5abb6f9ad7a5063fe71d81bc",
            "5abb6f9bd7a5063fe71d8317",
            "5ad56ecc1a586701671ea562",
            "5aa0b504efcd4859d55577a1",
            "5aa0b47a5f148c5def64fd51",
            "5bf7c2a47ecfe4033d635962",
            "5ac5830725583c1a9f607127",
            "5af1221c1a58670dc95563b1",
            "5abb6f9bd7a5063fe71d82cd",
            "5bbda928e5937819865b1831",
            "5b07d221738a462e6b2114d1",
            "5cac262674360266617747d4",
            "5ae06d98efcd484eee7dcb73"
        ]
        pageId = randomItem(pageIds)
        header = webHeader(self)
        response = self.client.get("/int/pages/%s" % pageId,  name="/int/pages/[id]", headers=header)

    @seq_task(2)
    def storeShow(self):
        storeId = randomItem(webStoreIds)
        header = {
            **commonHeader(self),
            **jwtHeader(self)
        }
        response = self.client.get("/v3/stores/%i" % storeId,  name="/v3/stores/[id]", headers=header)

    # @seq_task(3)
    # def webStoreRedirect(self):
    #     affiliateIds = [56336,56099,55416,32390,51300,34486,55428,55432,55438,55440,55420,56203,56792,56066,56927,56775,56786,56821,56764,56552,56831]
    #     affiliateId = randomItem(affiliateIds)
    #     header = webHeader(self)
    #     availableStores = [
    #         { "storeaffiliateId": 56099, "storeId": 2480 },
    #         { "storeaffiliateId": 55416, "storeId": 2093 },
    #         { "storeaffiliateId": 51300, "storeId": 1695 },
    #         { "storeaffiliateId": 55428, "storeId": 1643 },
    #         { "storeaffiliateId": 55432, "storeId": 1640 },
    #         { "storeaffiliateId": 55440, "storeId": 1634 },
    #         { "storeaffiliateId": 55420, "storeId": 1631 },
    #         { "storeaffiliateId": 29157, "storeId": 1630 },
    #         { "storeaffiliateId": 56203, "storeId": 1025 },
    #         { "storeaffiliateId": 56936, "storeId": 1012 },
    #         { "storeaffiliateId": 56066, "storeId": 671 },
    #         { "storeaffiliateId": 56927, "storeId": 661 },
    #         { "storeaffiliateId": 56775, "storeId": 318 },
    #         { "storeaffiliateId": 56786, "storeId": 271 },
    #         { "storeaffiliateId": 56552, "storeId": 93 },
    #         { "storeaffiliateId": 56831, "storeId": 102 }
    #     ]
    #     store = randomItem(availableStores)
    #     response = self.client.post(
    #         "/int/shoppingtrips",
    #         json={
    #             "accountId": self.accountId,
    #             "storeId": store["storeId"],
    #             "storeaffiliateId": store["storeaffiliateId"],
    #             "browserName": "Chrome",
    #             "browserVersion": "53.0",
    #             "browserPlatform": "Apple Mac",
    #         },
    #         headers=header
    #     )

    # @seq_task(4)
    # def specialstores(self):
    #     header = webHeader(self)
    #     response = self.client.get("/int/specialstores",  name="/int/specialstores", headers=header)

    @seq_task(5)
    def referrals(self):
        #responseCacheable
        header = webHeader(self)
        response = self.client.get("/int/referrals/getByAccountId?accountId=%s&requestDomain=%s" % (self.accountId , self.env['domain'] ), name="/int/referrals/getByAccountId[id]", headers=header)

    def switchAccount(self):
        randomAccount = randomItem(accounts)
        self.accountId = randomAccount["_id"]
        self.accountUUID = randomAccount["uuid"]
        self.device = getRandomDevice()
        self.env = getEnv()

class OverviewBehavior(TaskSequence):

    def on_start(self):
        self.switchAccount()

    # @seq_task(1)
    # def loadingCashbackPage(self):
    #     self.switchAccount()
    #     self.latestCashback()
    #     self.overviewCashbacks()

    # def latestCashback(self):
    #     header = {
    #         **commonHeader(self),
    #         **jwtHeader(self)
    #     }
    #     response = self.client.get("/cashbacks/latest", headers=header)

    # def overviewCashbacks(self):
    #     #responseCacheable
    #     header = {
    #         **commonHeader(self),
    #         **jwtHeader(self)
    #     }
    #     response = self.client.get("/overview/cashbacks", headers=header)

    @seq_task(2)
    def cashbackIndex(self):
        #responseCacheable
        header = commonHeader(self)
        response = self.client.get("/v1/cashbacks?accountUuid=%s" % self.accountUUID, name="/v1/cashbacks?accountUuid=[id]", headers=header)

    def switchAccount(self):
        randomAccount = randomItem(accounts)
        self.accountId = randomAccount["_id"]
        self.accountUUID = randomAccount["uuid"]
        self.device = getRandomDevice()

class AppBehavior(TaskSequence):
    def on_start(self):
        self.switchAccount()

    @seq_task(1)
    def load(self):
        self.switchAccount()
        self.banner()
        # self.storePushDevice()
        self.serviceConfigurations()

    def banner(self):
        header = {
            **commonHeader(self),
            **jwtHeader(self)
        }
        response = self.client.get("/mobile/banners", headers=header)

    def storePushDevice(self):
        header = commonHeader(self)
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

    def serviceConfigurations(self):
        header = commonHeader(self)
        response = self.client.get("/mobile/services/configurations", headers=header)

    @seq_task(2)
    def storeIndex(self):
        header = commonHeader(self)
        response = self.client.get("/mobile/stores/", headers=header)

    @seq_task(3)
    def topDeal(self):
        header = commonHeader(self)
        response = self.client.get("/mobile/top-deals", headers=header)

    @seq_task(4)
    def topDealWithStoreId(self):
        storeId = randomItem(storeIds)
        header = commonHeader(self)
        response = self.client.get("/mobile/top-deals?store_id=%i" % storeId, name="/mobile/top-deals?store_id=[id]", headers=header)

    @seq_task(5)
    def campaigne(self):
        header = commonHeader(self)
        response = self.client.get("/mobile/campaigns", headers=header)

    @seq_task(6)
    def wordpressPosts(self):
        if self.env["sid"] == "AU":
            return
        #responseCacheable
        header = {
            **commonHeader(self),
            **jwtHeader(self)
        }
        response = self.client.get("/mobile/wordpress-posts", headers=header)

    @seq_task(7)
    def storeRedirect(self):
        affiliateIds = [11663, 8448, 11662, 8448, 11631, 8439, 11638, 8439, 11707, 8007, 11767, 8432, 11705, 8448, 11703, 8448, 11768, 8393, 7875, 8371, 7885, 8141, 11762, 8379, 11714, 7920, 11314, 8362, 11857, 7766, 11666, 7921, 11300, 8437, 11851, 7762, 11654, 8106, 11765, 9036, 11733, 7927, 11655, 8272, 11658, 7791, 11737, 7878, 11741, 7878, 11730, 7912, 10640, 8913, 11656, 7768, 11716, 8247, 11657, 8266, 7828, 8433, 6889, 8416, 11717, 7767, 10933, 8041, 6771, 7953, 8990, 8223, 10950, 8005, 10782, 8006, 6687, 8440, 8862, 8442, 10661, 8245, 9659, 8440, 10576, 7761, 6215, 8350, 7879, 8354, 11735, 7723, 3858, 7646]
        affiliateId = randomItem(affiliateIds)
        header = {
            **commonHeader(self),
            **jwtHeader(self)
        }
        response = self.client.get(
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

    def switchAccount(self):
        randomAccount = randomItem(accounts)
        self.accountId = randomAccount["_id"]
        self.accountUUID = randomAccount["uuid"]
        self.device = getRandomDevice()
        self.env = getEnv()

#User
class WebUser(HttpUser):
    weight=3
    tasks = [WebBehavior]
    min_wait = 1000
    max_wait = 1000

class AppUser(HttpUser):
    weight=5
    tasks = [AppBehavior]
    min_wait = 1000
    max_wait = 1000

class OverviewUser(HttpUser):
    weight=2
    tasks = [OverviewBehavior]
    min_wait = 1000
    max_wait = 1000
