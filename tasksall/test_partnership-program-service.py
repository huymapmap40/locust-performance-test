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
    def getPartnershipEnrollments(self):
        self.client.get(
            url='/v1/partnership-programs/enrollments/2939750'
        )

    @task(1)
    def getPartnershipDetail(self):
        headers = self.getRandomUserHeaders();
        self.client.get(
            url='/v3/partnership-programs/loadtest-staging-th',
            headers=headers,
        )

    @task(1)
    def getPartnershipDetailPowerscreen(self):
        headers = self.getRandomUserHeaders();
        self.client.get(
            url='/v3/partnership-programs/loadtest-staging-th/powerscreen',
            headers=headers,
        )

    @task(1)
    def getUserEnrolledPartnership(self):
        headers = self.getRandomUserHeaders();
        self.client.get(
            url='/v1/partnership-programs/me',
            headers=headers,
        )

    @task(1)
    def enrollInternal(self):
        payload = {
            'accountId': self.getRandomAccountId(),
            'code': 'loadtest'
        }
        self.client.post(
            url='/v1/partnership-programs/enroll',
            json=payload
        )

    @task(1)
    def enrollExternal(self):
        payload = {
            'code': 'loadtest-staging-th'
        }
        headers = self.getRandomUserHeaders()
        self.client.post(
            url='/v1/partnership-programs/enroll-external',
            json=payload,
            headers=headers,
        )

    @task(1)
    def getExternalMembershipList(self):
        headers = self.getRandomUserHeaders()
        self.client.get(
            url='/v1/partnership-programs/externalMembership',
            headers=headers,
        )


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
