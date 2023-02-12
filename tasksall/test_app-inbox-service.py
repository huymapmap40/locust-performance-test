import base64
import random
from locust import HttpUser, TaskSet, task, between

COUNTRY = "SG"
PATH_GET_COUNT = "/v1/inbox/count"
PATH_GET_MESSAGES = "/v1/inbox/messages"

weight_d = {
    "AU": {
        PATH_GET_COUNT: 85,
        PATH_GET_MESSAGES: 12,
    },
    "ID": {
        PATH_GET_COUNT: 85,
        PATH_GET_MESSAGES: 12,
    },
    "KR": {
        PATH_GET_COUNT: 87,
        PATH_GET_MESSAGES: 10,
    },
    "MY": {
        PATH_GET_COUNT: 85,
        PATH_GET_MESSAGES: 10,
    },
    "PH": {
        PATH_GET_COUNT: 82,
        PATH_GET_MESSAGES: 13,
    },
    "SG": {
        PATH_GET_COUNT: 90,
        PATH_GET_MESSAGES: 7,
    },
    "TH": {
        PATH_GET_COUNT: 82,
        PATH_GET_MESSAGES: 13,
    },
    "TW": {
        PATH_GET_COUNT: 80,
        PATH_GET_MESSAGES: 16,
    },
    "VN": {
        PATH_GET_COUNT: 78,
        PATH_GET_MESSAGES: 18,
    },
}

def getUserHeaders(account_id: int) -> dict:
    account = '{"id":' + f'{account_id}' + '}'
    encodedBytes = base64.b64encode(account.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    headers ={
        "Authorization": encodedStr
    }
    return headers

def get_account_id() -> int:
    return random.randint(1, 120000000)

class UserBehavior(TaskSet):
    @task(weight_d[COUNTRY][PATH_GET_COUNT])
    def getUnreadCount(self):
        headers = getUserHeaders(get_account_id())
        self.client.get(
            url=PATH_GET_COUNT,
            headers=headers
        )

    @task(weight_d[COUNTRY][PATH_GET_MESSAGES])
    def getMessages(self):
        headers = getUserHeaders(get_account_id())
        self.client.get(
            url=PATH_GET_MESSAGES,
            headers=headers
        )

class WebsitUser(HttpUser):
    wait_time = between(1, 3)
    tasks =  [UserBehavior]
