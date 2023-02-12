from locust import HttpUser, TaskSet
import base64
import random
import json
import uuid
import string
from dataprovider_staging_sg import *


# Test Preparation
# 1. Remove Rule: 'isValidEcommerceOrder' and 'hasVerifiedAccountEmail' from ecommerce payee config { "config.strategy": 'ecommerce-payment'})
# 2. Clear ecommerce payee config cache:(del payeeconfigs:ecommerce)
# 3. Update withdrawal opsconfig 'value.maximumDailyWithdrawalLimit' to be very huge number
# 4. Clear withdrawal opsconfig Cache: (del 'opsconfig:withdrawalrequests')

def getRandomOrderNumber(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def getRandomAccountId():
    position = random.randint(0, len(ACCOUNTS) - 1)
    return str(ACCOUNTS[position])

def getUserHeaders(user):
    account = '{"id":'+ str(user) +'}';
    encodedBytes = base64.b64encode(account.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    headers ={
        "X-Request-Id":"1c105757-9713-45bc-bbef-4ccf6ff62d9b",
        "X-Shopback-Agent":"sbandroidagent/1.0",
        "X-Shopback-Build":"2700000",
        "X-Device-Id":"00000000-0000-0000-0000-000000000000",
        "X-Shopback-Client-User-Agent":"00000000-0000-0000-0000-000000000000",
        "X-Shopback-Device-Model":"Android",
        "X-Shopback-Domain":"www.shopback.sg",
        "X-Shopback-Key":"q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Language":"en",
        "x-load-test": '4302291891',
        "X-Shopback-Member-Access-Token":"43738946fc2c86306c561cc43b04c2c3%3Aa6161f076397db0f2f479b7e698ba02b3ca962a90c244ab02217171f3a035f3b62b9bee9d24fcc4e301ee9c8340e6a45",
        "Authorization": 'JWT ' + encodedStr,
        "user-agent": "ShopBack/2.70.0 (com.shopback.ShopBack; build:2700000; iOS 13.4.1) Alamofire/4.8.2"
        }
    return headers

# obsolete
def makeEcommercePayment(l):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    refId = str(uuid.uuid4())
    orderNumber = getRandomOrderNumber(10)

    data = {
        "order": {
            "amount": 0.000001,
            "refId": refId,
            "orderNumber": orderNumber
        },
        "commit": "true"
    }

    with l.client.post(
        url='/withdrawals/withdrawalrequests/make-payment',
        json=data,
        headers=h,
        catch_response=True
    ) as response:
        print('%s user id: %s - Response Status %s'%('makeEcommercePayment', accountId, str(response.status_code)))
        if response.status_code in [200, 400, 429]:
            response.success()
        else:
            response.failure('Unexpect Response Status %s'%(response.status_code))

def getPayees(l):
    accountId = getRandomAccountId()
    response = l.client.get(
        url='/payees?accountId=' + accountId + '&limit=1000',
        name="/payees?accountId=xxx&limit=1000"
    )
    print('%s user id: %s - Response Status %s'%('getPayees', accountId, str(response.status_code)))

def getOverview(l):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    response = l.client.get(
        url='/withdrawals/overview/withdrawalrequests',
        headers=h
    )
    print('%s user id: %s - Response Status %s'%('getOverview', accountId, str(response.status_code)))

# new tests
# GET /withdrawals/payout/history => simulate API call from westeros withdrawal list
# GET /withdrawals/options/payeeconfigs => simulate API call from westeros cashout page payee config section
# GET /withdrawals/options/payees => simulate API call from westeros cashout page payee selection section
# POST /withdrawals/withdrawalrequests => simulate API call from westeros cashout make withdrawal request form submit

def getPayoutHistory(self):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    response = self.client.get(
        url='/withdrawals/payout/history?startDate=2019-01-01T00:00:00&endDate=2022-07-07T00:00:00&limit=100',
        name='/withdrawals/payout/history',
        headers=h
    )
    print('%s user id: %s - Response Status %s'%('getPayoutHistory', accountId, str(response.status_code)))

def getPayeeConfigs(self):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    response = self.client.get(
        url='/withdrawals/options/payeeconfigs',
        headers=h
    )
    print('%s user id: %s - Response Status %s'%('getPayeeConfigs', accountId, str(response.status_code)))

def getPayee(self):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    response = self.client.get(
        url='/withdrawals/options/payees',
        headers=h
    )
    print('%s user id: %s - Response Status %s'%('getPayee', accountId, str(response.status_code)))

def makeWithdrawalRequest(self):
    accountId = getRandomAccountId()
    h = getUserHeaders(accountId)
    refId = str(uuid.uuid4())
    orderNumber = getRandomOrderNumber(10)

    payee = [p for p in PAYEES if p['accountId'] == accountId]
    if len(payee) > 0:
        payee = payee[0]
    else:
        payee = PAYEES[random.randint(0, len(PAYEES) - 1)]

    data = {
        "payee": {
            "_id": payee["_id"]
        },
        "form": {
            "amount": 10
        },
        "otp": {
            "request_id": refId
        },
        "commit": "true"
    }

    with self.client.post(
        url='/withdrawals/withdrawalrequests',
        json=data,
        headers=h,
        catch_response=True
    ) as response:
        print('%s user id: %s - Response Status %s'%('makeWithdrawalRequest', accountId, str(response.status_code)))
        if response.status_code in [200, 400, 429]:
            response.success()
        else:
            response.failure('Unexpect Response Status %s'%(response.status_code))

class UserBehavior(TaskSet):
    tasks = {
        # makeEcommercePayment: 5, # 20 RPM ON PROD
        # getPayees: 10,  # 50 RPM ON PROD
        # getOverview: 85 # 400 RPM on PROD 
        getPayoutHistory: 85,
        getPayeeConfigs: 10,
        getPayee: 10,
        makeWithdrawalRequest: 5
    }

class WithdrawalServiceUser(HttpUser):
    tasks =  [UserBehavior]

    min_wait = 1000
    max_wait = 3000
