from locust import HttpUser, TaskSet
import random

_ACTIVE_TIME = "2019-08-08T00:00:00.000Z"


def getRandomStoreIdForV1():
    return random.randint(500, 2700)


def getRandomStoreIdForV2():
    return random.randint(1, 995)


def getV1ActiveCommercials(self):
    storeId = getRandomStoreIdForV1()
    endpoint = "/rat/v1/activecommercials?storeId=%s&activeTime=%s" % (
        storeId, _ACTIVE_TIME)
    self.client.get(endpoint)


def getV2ActiveCommercialsForOneStore(self):
    storeId = getRandomStoreIdForV2()
    endpoint = "/rat/v2/activecommercials?storeIds=%s&activeTime=%s" % (
        storeId, _ACTIVE_TIME)
    self.client.get(endpoint, name="/v2/activecommercials")


class UserBehavior(TaskSet):
    tasks = {
        getV2ActiveCommercialsForOneStore: 1
        # getV1ActiveCommercials: 1
    }


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 300
    max_wait = 2400
