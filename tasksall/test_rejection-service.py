
from locust import HttpLocust, TaskSet,  HttpUser, TaskSequence, seq_task
import base64
import random


def getRandomCashbackIds():
    cashbackIdSource = [
            '23669895',
            '23669892',
            '23669871',
            '23669868',
            '23669866',
            '23669858'
        ]

    elements_num = random.randint(1, len(cashbackIdSource) - 1)
    self.cashbackIds = random.sample(cashbackIdSource, elements_num)    
    return random.sample(cashbackIdSource, elements_num)
def getRejectionReasons(l):
    cashbackIds = getRandomCashbackIds()
    queryString = '&cashbackIds='.join(
            str(cashbackId) for cashbackId in cashbackIds)

    cacheValue = "no-cache" if random.randint(0, 1) == 0 else "cache"
    header = {
        "Cache-Control": cacheValue
    }
    response = l.client.get(
        url = '/cr2/reasons?cashbackIds='+queryString,
        headers = header
    )
    result = response.json()
    print(result)

class UserBehavior(TaskSet):
    tasks = {
        getRejectionReasons: 1
    }

class RejectionServiceUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000

    @seq_task(1)
    def spam(self):

        cacheValue = "no-cache" if random.randint(0, 1) == 0 else "cache"
        header = {
            "Cache-Control": cacheValue
        }

        queryString = "&cashbackIds=".join(
            str(cashbackId) for cashbackId in self.cashbackIds)

        print("Spamming cashbackIds="+queryString+" with "+cacheValue)
        response = self.client.get(
            "/cr2/reasons?cashbackIds="+queryString, headers=header)
        print(response.text)


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 100
    max_wait = 500
