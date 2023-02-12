# coding=UTF-8
import random
import base64
import json
import csv
import string
import random
import uuid
from locust import HttpUser, TaskSet, task, between

# ./install.sh environments/test_notification.yaml test sb-dep-dev-team-user-comm
# ./forward.sh sb-dep-dev-team-user-comm  
# ./remove.sh sb-dep-dev-team-user-comm    

TW_DOMAIN = 'www.shopback.com.tw'
TW_LANG = 'zh'
TW_TIMEZONE = 'Asia/Taipei'

AU_DOMAIN = 'www.shopback.com.au'
AU_LANG = 'en'
AU_TIMEZONE = 'Australia/Perth' 

ID_DOMAIN = 'www.shopback.co.id'
ID_LANG = 'id'
ID_TIMEZONE = 'Asia/Jakarta'


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def get_jwt(self, account_id):
        authorization_content = json.dumps({
            "uuid": "479c94048a8e410694ea24fc17302906",
            "iss": ID_DOMAIN,
            "issuedAt": 1577477107.184,
            "iat": 1577477107,
            "exp": 1578773107,
            "id": account_id
        })
        jwt = base64.b64encode(
            authorization_content.encode('utf-8')).decode('utf-8')
        jwt_value = 'JWT {}'.format(jwt)

    def get_account_id(self):
    #     return random.choice(data)[0]
        # return random.choice([206342111,200000083] )
        return random.randint(7000000000, 8000000000)

    def get_device_id(self):
        deviceSuffix_list = random.randint(1000000, 9999999)
        device_id = 'abcde{}'.format(deviceSuffix_list)
        return device_id

    def get_device(self):
        devices = [
            {'agent': 'sbandroidagent', 'type': 'Android', 'model': 'H9493', 'os': '10'},
            {'agent': 'sbiosagent', 'type': 'iOS', 'model': 'iPhone', 'os': '14.6'}
        ]
        return random.choice(devices)

    @task
    def upsert_device(self):
        client = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        idempotentId = str(uuid.uuid4())
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = {
            "client": client,
            "emailNotification": {
                "campaignId":"67631288-5287-e609-77e7-c484054b5a40",
                "list": [
                    {
                        "accountId": 101828960,
                        "options": [
                            {
                                "name": "age",
                                "value": "11"
                            },
                            {
                                "name": "name",
                                "value": "name for user"
                            }
                        ]
                    }
                ],
                "vendor":"Braze",
                "brazeOption":{
                    "applicationGroup":"general",
                    "campaignType":"transactional"
                }
            },
            "idempotentId": idempotentId
        }
        # print(headers)
        # print(payload)
        self.client.post(
            "/notification", 
            json=(payload),
            headers=headers, 
            name="/notification"
        )
        self.client.close()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior,]
    wait_time = between(1, 3)
