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
            "X-Shopback-Build": "99999999"
        }
        return headers

    def getRandomUserHeaders(self):
        ran = random.randint(1000000000, 2000000000)
        return self.getUserHeaders(ran)

    def getPreDefinedUsersHeaders(self):
        return self.getUserHeaders(5213064)

    # SBOC Home: 83.80%
    # Assumed there are two API calls
    challengeComponentWithoutCachedEntryConditionWeight = 168

    # Challenge Home: 42.60%
    challengeHomeListWithoutCachedEntryConditionWeight = 43
    perkPartnershipMerchantProgramWeight = 43
    perkMerchantChallengesWeight = 43
    perkPartnershipChallengeWeight = 43

    # Challenge Detail: 26.50%
    challengeDetailWithoutCachedEntryConditionWeight = 27

    currentChallengeWeight = 50

    # challengeComponentWithCachedEntryConditionWeight = 10
    # challengeHomeListWithCachedEntryConditionWeight = 3
    # challengeDetailWithCachedEntryConditionWeight = 2

    @task()
    def currentChallengeForWeb(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url="/v2/challenges/current-challenges?limit=20&offset=0",
            headers=headers
        )

    @task(challengeComponentWithoutCachedEntryConditionWeight)
    def challengeComponentWithoutCachedEntryCondition(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/v2/challenges?codes=SG_2021-11_SBOC_FTM_0_5_MC_0_0_0_AGODA&customSorts=codesFilter&statuses=NOT_STARTED,OPTED_IN,IN_PROGRESS,ACTION_COMPLETED,GOAL_COMPLETED',
            headers=headers
        )

    @task(challengeDetailWithoutCachedEntryConditionWeight)
    def challengeDetailWithoutCachedEntryCondition(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url='/earn-more/v4/challenges/LOADTEST_2022_STAGING',
            headers=headers
        )

    # @task(perkPartnershipMerchantProgramWeight)
    # def perkPartnershipMerchantProgram(self):
    #     headers = self.getPreDefinedUsersHeaders()
    #     self.client.post(
    #         url="/v2/challenges/partnership-merchant-programs",
    #         headers=headers
    #     )

    @task(perkMerchantChallengesWeight)
    def perkMerchantChallenges(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url="/v2/challenges/merchant-challenges",
            headers=headers
        )

    @task(perkPartnershipChallengeWeight)
    def perkPartnershipChallenge(self):
        headers = self.getPreDefinedUsersHeaders()
        self.client.get(
            url="/v2/challenges/partnership-challenges",
            headers=headers
        )

    @task(1)
    def uhsChallenge(self):
        headers = self.getRandomUserHeaders()
        self.client.get(
            url='/v2/challenges/uhs-challenges?offset=0&limit=3&sortBy=rank',
            headers=headers
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 500
    max_wait = 1000
