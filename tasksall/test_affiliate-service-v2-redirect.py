from locust import HttpUser, TaskSet, task, between
import random
import json

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Authorization': 'Bearer eyJpZCI6NDkxOTUyN30=',
            'Content-Type': 'application/json',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
        }
        self.mobileAffiliateLinkIds = [99520, 99521, 308428, 308429, 63238, 71299, 99518, 99519, 99542, 99543, 113651, 113652, 308215]
        self.webAffiliateLinkIds = [308427, 58063, 63238, 71299, 308404, 51389, 308215, 50915, 308408, 308384]
        self.payload = {
            'browserName': 'Chrome',
            'browserVersion': '1.0.0',
            'browserPlatform': 'Mac',
            'advertisingId': '78ccb948',
            'referrerUrl': 'store',
            'appsflyerId': '1234',
            'platformTrackingId': '1234'
        }

    @task(1)
    def webRedirect(self):
        affiliateLinkId = random.choice(self.webAffiliateLinkIds)
        self.headers['X-Shopback-Agent'] = random.choice(['sbconsumeragent/1.0', 'sbmwebagent/1.0'])
        
        self.client.post(
            url='/v2/affiliate-links/' + str(affiliateLinkId) + '/redirect',
            headers=self.headers,
            json=self.payload
        )

    @task(1)
    def mobileRedirect(self):
        affiliateLinkId = random.choice(self.mobileAffiliateLinkIds)
        self.headers['X-Shopback-Agent'] = random.choice(['sbiosagent/1.0', 'sbandroidagent/1.0'])
        
        self.client.post(
            url='/v2/affiliate-links/' + str(affiliateLinkId) + '/redirect',
            headers=self.headers,
            json=self.payload
        )


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(5, 10)
