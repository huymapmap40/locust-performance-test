import json
import base64
import random
import uuid
import string

from locust import HttpUser, TaskSet, task, between


with open('/locust-tasks/withdrawal_accounts.txt', 'r') as f:
  _ACCOUNT_IDS = list(map(int, f.read().splitlines()))

def getRandomId():
  return random.choice(_ACCOUNT_IDS)

def getRandomOrderNumber(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def fakeAuthToken(id):
  tokenContent = b"{\"id\":%d}" % (id)
  encodedToken = base64.b64encode(tokenContent)
  return encodedToken.decode('ascii')

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.client.verify = False
        self.id = getRandomId()
        self.token = fakeAuthToken(self.id)
        self.uuid = str(uuid.uuid4())

        self.headers = {
            'x-shopback-context-user': json.dumps({ 'id': self.id, 'jwtToken': self.token, 'uuid': self.uuid })
        }

    @task(50)
    def requestWithdrawalsListPage(self):
        # test on withdrawal fragment
        slug = '/payment-history'
        with self.client.get(
            url=slug,
            allow_redirects=False,
            catch_response=True,
            headers=self.headers
        ) as response:
            print(slug, self.id, response.status_code)
            response.success()

    @task(30)
    def requestWithdrawalsPayoutHistoryApi(self):
        # test on withdrawal requests endpoint via api-gateway
        # go through http://api-gateway/withdrawals/payout/history
        slug = '/wes-api/withdraw/payment-history'
        with self.client.get(
            url=slug,
            allow_redirects=False,
            catch_response=True,
            headers=self.headers
        ) as response:
            print('%s user id: %s - Response Status %s'%('requestWithdrawalsPayoutApi', self.id, str(response.status_code)))
            if response.status_code in [200, 400, 429]:
                response.success()
            else:
                response.failure('Unexpect Response Status %s'%(response.status_code))

    @task(10)
    def requestCashoutPage(self):
        # test on payee config via api gateway
        # test payees endpoint via api gateway
        # go through http://api-gateway/withdrawals/options/payeeconfigs and
        # go through http://api-gateway/withdrawals/options/payees
        slug = '/withdrawal-payment'
        with self.client.get(
            url=slug,
            allow_redirects=False,
            catch_response=True,
            headers=self.headers
        ) as response:
            print('%s user id: %s - Response Status %s'%('requestCashoutPage', self.id, str(response.status_code)))
            if response.status_code in [200, 429]:
                response.success()
            else:
                response.failure('Unexpect Response Status %s'%(response.status_code))

    @task(10)
    def requestCreateWithdrawal(self):
        # test on create withdrawal requests endpoint
        # go through 
        slug = '/wes-api/withdraw/withdraw-requests'
        data = {
            "order": {
                "amount": 0.000001,
                "refId": str(uuid.uuid4()),
                "orderNumber": getRandomOrderNumber(10)
            },
            "commit": "true"
        }
        with self.client.post(
            url=slug,
            json=data,
            allow_redirects=False,
            catch_response=True,
            headers=self.headers
        ) as response:
            print('%s user id: %s - Response Status %s'%('requestCreateWithdrawal', self.id, str(response.status_code)))
            if response.status_code in [200, 400, 429]:
                response.success()
            else:
                response.failure('Unexpect Response Status %s'%(response.status_code))
    

    @task
    def stop(self):
        self.interrupt()

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.3, 0.8)

