from locust import HttpUser, TaskSet

def getPayoutHistory(self):
    response = self.client.get(
        url='/wes-api/withdraw/payment-history'
    )
    print('%s - Response Status %s'%('/wes-api/payment-history', str(response.status_code)))

def withdrawalFormPage(self):
    response = self.client.get(
        url='/withdrawal-payment'
    )
    print('%s - Response Status %s'%('/withdrawal-payment', str(response.status_code)))

def makeWithdrawalRequest(self):
    response = self.client.post(
        url='/wes-api/withdraw/withdraw-requests'
    )
    print('%s - Response Status %s'%('/wes-api/withdraw/withdraw-requests', str(response.status_code)))

class UserBehavior(TaskSet):
    tasks = {
        getPayoutHistory: 85,
        withdrawalFormPage: 10,
        makeWithdrawalRequest: 5
    }

class WithdrawalServiceUser(HttpUser):
    tasks =  [UserBehavior]

    min_wait = 1000
    max_wait = 3000
