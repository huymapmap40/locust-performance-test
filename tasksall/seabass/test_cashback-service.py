import urllib
from cashback_dataprovider import ACCOUNTS
from locust import HttpUser, SequentialTaskSet, task
import random

def jwtHeader(accountId):
    front = '{"id"'
    back = str(accountId)+'}'
    urlencodedfront = urllib.parse.quote(front, safe='')
    urlencodedback = urllib.parse.quote(back, safe='')
    urlencoded = urlencodedfront+':'+urlencodedback
    print(urlencoded)

    return {"x-shopback-context-user": urlencoded }


class UserBehavior(SequentialTaskSet):
    def on_start(self):
        if len(ACCOUNTS) > 0:
          self.accountId = random.choice(ACCOUNTS)

    @task
    def listCustomerCashbacks(self):
        """List cutomer cashbacks"""
        headers = {**jwtHeader(self.accountId)}
        self.client.get(url="/wes-api/cashback-activity/history", headers=headers)

    @task
    def listCustomerCashbackFilters(self):
        """List cutomer cashback filters"""
        headers = {**jwtHeader(self.accountId)}
        self.client.get(url="/wes-api/cashback-activity/filters", headers=headers)

    
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 100
    max_wait = 1000