import json
import base64
import random

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def getUserHeaders(self, user):
        account = '{"id":'+ str(user) +'}'
        encodedBytes = base64.b64encode(account.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        headers ={
            "Authorization": encodedStr,
        }
        return headers

    def getRandomAccountId(self):
        return random.randint(1000000000, 2000000000)

    def getRandomUserHeaders(self):
        ran = self.getRandomAccountId()
        return self.getUserHeaders(ran)

    @task(15)
    def getCampaignById(self):
        campaignId = '63048ac046ba06a8f82a54bc' # existing campaign in staging-sg
        headers = self.getRandomUserHeaders()
        self.client.get(
            url='/campaign-bonus/ext/campaign-bonus-segments/{}'.format(campaignId),
            headers=headers,
        )

    @task(15)
    def enrollUser(self):
        campaignId = '630360938e0b012fcc1f6a13' # existing campaign in staging-sg
        headers = self.getRandomUserHeaders()
        payload = {
            'accountId': self.getRandomAccountId(),
            'campaignId': campaignId
        }
        self.client.post(
            url='/campaign-bonus/ext/campaign-bonus-segments/enroll',
            headers=headers,
            json=payload,
        )

    @task(100)
    def getMerchantPartnershipProgramInfo(self):
        merchantId = '23204' # existing merchant in staging-sg
        headers = self.getRandomUserHeaders()

        self.client.get(
            url=f'/campaign-bonus/ext/campaign-bonus-segments/merchant-redirect/{merchantId}/program-info',
            headers=headers,
        )

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
