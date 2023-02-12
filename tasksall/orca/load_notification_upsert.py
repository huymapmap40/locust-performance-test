# coding=UTF-8
import random
import base64
import json
from locust import HttpUser, TaskSet, task, between

TW_DOMAIN = 'www.shopback.com.tw'
TW_LANG = 'zh'
TW_TIMEZONE = 'Asia/Taipei'

AU_DOMAIN = 'www.shopback.com.au'
AU_LANG = 'en'
AU_TIMEZONE = 'Australia/Perth' 

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def get_jwt(self, account_id):
        authorization_content = json.dumps({
            "uuid": "479c94048a8e410694ea24fc17302906",
            "iss": AU_DOMAIN,
            "issuedAt": 1577477107.184,
            "iat": 1577477107,
            "exp": 1578773107,
            "id": account_id
        })
        jwt = base64.b64encode(
            authorization_content.encode('utf-8')).decode('utf-8')
        jwt_value = 'JWT {}'.format(jwt)

    def get_account_id(self):
        return random.randint(7000000000, 8000000000)

    def get_device_id(self):
        deviceSuffix_list = random.randint(10000, 99999)
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
        account_id = self.get_account_id()
        jwt = self.get_jwt(account_id)
        device_id = self.get_device_id()
        device = self.get_device()
        app_version = '2.66.0-TEST'
        device_agent = '{}/{}'.format(device['agent'], app_version)
        token = "6exwK7MpMvOs:APA91bFOzUHMwSQV4cCJILnpcDN80m_tQRsPqKE_wJETpf03e2_cJxPhoEhvgJc50p04IRF0L-MYlhVIJG1UMsD-aBANgBH8p7aQPf8FzE8iFU3MGg5P1HGCsYbceGSR{}".format(account_id)
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": jwt,
            "X-Shopback-Agent": device_agent,
            "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
            "X-Device-Id": device_id,
            "X-Shopback-Domain": AU_DOMAIN,
            "X-Shopback-Language": AU_LANG,
            "X-Shopback-Client-User-Agent": device_id
        }

        payload = {
            "deviceType": device['type'],
            "accountId": str(account_id),
            "appVersion": app_version,
            "alertPriceDrop": True,
            "alertPayment": True,
            "alertCashback": True,
            "timeZone": AU_TIMEZONE,
            "deviceId": device_id,
            "deviceModel": device['model'],
            "deviceOS": device['os'],
            "deviceToken": token
        }
        print(headers)
        print(payload)
        self.client.post(
            "/device", 
            json=(payload),
            headers=headers, 
            name="/device"
        )
        self.client.close()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior,]
    wait_time = between(1, 3)
