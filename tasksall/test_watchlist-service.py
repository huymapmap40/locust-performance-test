from locust import HttpUser, TaskSet, task
import logging
import random

# TW merchants
MERCHANT_IDS = [20013, 20014, 20015, 20016, 20017, 20018, 20019, 20020, 20021, 20022, 20023, 20024, 20025,
                20026, 20027, 20028, 20029, 20030, 20031, 20032, 20033, 20034, 20035, 20036, 20037, 20038, 20039, 20040]

MERCHANT_IDS_FOR_GET = [20041, 20042, 20043, 20044, 20045, 20046, 20047, 20048, 20049, 20050,
                        20051, 20052, 20053, 20054, 20055, 20056, 20057, 20058, 20059, 20060]

REMINDER_TYPE = ['store', 'product']
RECOMMEND_MERCHANT_TYPE = ['onboarding', 'personalized', 'home']

# SG merchants
# MERCHANT_IDS = [17815, 17816, 17817, 17818, 17819, 17820, 17821, 17822, 17823, 17824,
#                 17825, 17826, 17827, 17828, 17829, 17830, 17831, 17832, 17833, 17834,
#                 17835, 17836, 17837, 17838, 17839, 17840, 17841, 17842]

# MERCHANT_IDS_FOR_GET = [17844, 17845, 17846, 17847, 17848, 17849, 17850, 17851, 17852, 17853,
#                         17854, 17855, 17856, 17857, 17858, 17859, 17860, 17861, 17862, 17863]


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'X-Shopback-Domain': 'www.shopback.com.tw',
            'X-Shopback-Agent': 'sbiosagent/3.20.0-SNAPSHOT',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'x-shopback-recaptcha-type': 'bypass',
            'x-shopback-build': '3800000'
        }

        payload = {
            "email": "1111load+test{}@shopback.com".format(random.randint(1, 1000)),
            "password": ""
        }

        # get access token
        response = self.client.post(url="http://coral-edge.sb-dep-dev-team-zeus.svc.cluster.local/members/sign-in",
                                    headers=self.headers, json=payload)
        res = response.json()
        self.headers['Authorization'] = "JWT {}".format(res['auth']['access_token'])

        # make the token contain id data
        responseAuth = self.client.post(url="http://coral-edge.sb-dep-dev-team-zeus.svc.cluster.local/members/v2/oauth/validate",
                                        headers=self.headers)
        resAuth = responseAuth.json()
        self.headers['Authorization'] = "JWT {}".format(resAuth['accessToken'])
        # logging.info('Login with %s email and %s password',
        #              payload['email'], self.headers['Authorization'])

    @task(1)
    def addDeleteMerchant(self):

        payload = {
            "ids": MERCHANT_IDS,
        }
        with self.client.put(url="/v1/watchlist/merchant",
                             headers=self.headers, json=payload, catch_response=True) as response:
            self.isSuccess(response)
        with self.client.request(method="DELETE", url="/v1/watchlist/merchant",
                                 headers=self.headers, json=payload, catch_response=True) as responseDel:
            self.isSuccess(responseDel)
        self.client.close()

    @task(1)
    def getAggregationData(self):
        with self.client.get(url="/v1/watchlist/merchant",
                             headers=self.headers, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def queryMerchant(self):
        payload = {
            "ids": MERCHANT_IDS,
        }
        with self.client.post(url="/v1/watchlist/merchant/check",
                              headers=self.headers, json=payload, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def getRecommendMerchant(self):
        paras = {
            "type": random.choice(RECOMMEND_MERCHANT_TYPE)
        }
        with self.client.get(url="/v1/watchlist/recommend/merchant",
                             headers=self.headers, params=paras, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def getProactiveRecommendMerchant(self):
        paras = {
            "merchantId": random.choice(MERCHANT_IDS_FOR_GET)
        }
        with self.client.get(url="/v1/watchlist/recommend/proactive/setting/merchant",
                             headers=self.headers, params=paras, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def putProactiveRecommendMerchant(self):
        payload = {
            "hasShownDialog": True,
            "merchantId": random.choice(MERCHANT_IDS)
        }
        with self.client.put(url="/v1/watchlist/recommend/proactive/setting/merchant",
                             headers=self.headers, json=payload, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def getSimilarMerchant(self):
        paras = {
            "merchantId": random.choice(MERCHANT_IDS_FOR_GET)
        }
        with self.client.get(url="/v1/watchlist/recommend/similar/merchant",
                             headers=self.headers, params=paras, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def getRecoMerchant(self):
        paras = {}
        if random.uniform(0, 1) < 0.5:
            paras = {}

        with self.client.get(url="/v1/watchlist/recommend/reco/merchant",
                             headers=self.headers, params=paras, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(2)
    def getHighlightReminder(self):
        with self.client.get(url="/v1/watchlist/notification/reminder",
                             headers=self.headers, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(2)
    def putHighlightReminder(self):
        payload = {
            "type": random.choice(REMINDER_TYPE)
        }
        with self.client.put(url="/v1/watchlist/notification/reminder",
                             headers=self.headers, json=payload, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    @task(1)
    def postUserExperiment(self):
        payload = {
            "testKey": [
                "tw-watchlist-test1",
                "tw-watchlist-test2",
                "non-target-test",
                "inactive-test"
            ]
        }
        with self.client.post(url="/v1/watchlist/experiment/expose",
                             headers=self.headers, json=payload, catch_response=True) as response:
            self.isSuccess(response)
        self.client.close()

    def isSuccess(self, response):
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
            response.success()
        if response.status_code == 500 or response.status_code == 503:
            body = response.json()
            logging.info('fail" %s ', body['error']['message'])
            logging.info('fail" %s ', body['error']['code'])


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 3000
