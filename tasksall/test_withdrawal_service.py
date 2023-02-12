import base64
import random

from locust import HttpLocust, TaskSet

with open('/locust-tasks/withdrawal_accounts.txt', 'r') as f:
  _ACCOUNT_IDS = list(map(int, f.read().splitlines()))

_GET_PAYEES_LIMIT = 100

def getRandomId():
  return random.choice(_ACCOUNT_IDS)

def fakeAuthToken(id):
  tokenContent = b"{\"id\":%d}" % (id)
  encodedToken = base64.b64encode(tokenContent)
  return encodedToken.decode('ascii')

def healthCheck(self):
	self.client.get("/health")

# Called by Cashback Sync only!
def getPayees(self):
  endpoint = "/payees?accountId=%d&limit=%d" % (self.userId, _GET_PAYEES_LIMIT)
  self.client.get(endpoint, name="/payees?accountId&limit")

# Called by account-service to populate total in samantha
def getWithdrawalRequest(self):
  endpoint = "/withdrawals/overview/withdrawalrequests"
  self.client.get(endpoint, headers={
    "Authorization": self.authToken
  })

# Incomplete
def postWithdrawalRequest(self):
  endpoint = "/withdrawals/overview/withdrawalrequests"
  self.client.get(endpoint, headers={
    "Authorization": self.authToken
  })

def getWithdrawalPayoutHistory(self):
  endpoint = "/withdrawals/payout/history?startDate=2019-01-01T00:00:00&endDate=2019-07-01T00:00:00&limit=100"
  self.client.get(endpoint, headers={
    "Authorization": self.authToken
  })

def getPayeeConfigs(self):
  endpoint = "/withdrawals/options/payeeconfigs"
  self.client.get(endpoint)

def getPayeesOptions(self):
  endpoint = '/withdrawals/options/payees'
  self.client.get(endpoint, headers = {
    "Authorization": self.authToken
  })

class UserBehavior(TaskSet):
  def on_start(self):
    numAccountIdsLeft = len(_ACCOUNT_IDS)
    if numAccountIdsLeft > 0:
      self.userId = _ACCOUNT_IDS.pop(random.randint(0, numAccountIdsLeft - 1))
      self.authToken = "JWT %s" % fakeAuthToken(self.userId)
    else:
      self.userId = random.randint(1000000, 3000000)
      self.authToken = fakeAuthToken(self.userId)

  tasks = {
    getWithdrawalRequest:196,
    getWithdrawalPayoutHistory:4,
    getPayeeConfigs:4,
    getPayeesOptions:5
  }

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 300
    max_wait = 2400
