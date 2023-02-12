import json
from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'Host': 'bob-iris.gameloft.com',
            'Origin': 'https://oms.gameloft.com',
            'Referer': 'https://oms.gameloft.com/'
        }
        self.headers2 = {
            'Host': 'iris07-gold-ssl-gzip.gameloft.com',
            'Referer': 'https://iris07-gold-ssl-gzip.gameloft.com/3402/loader_1534214233.23.html'
        }
        self.headers3 = {
            'Host': 'oms.gameloft.com',
            'Origin': 'https://oms.gameloft.com',
            'Referer': 'https://oms.gameloft.com/',
            'Content-type': 'application/json'
        }

    @task
    def get_main(self):
        self.client.get(
            url='https://oms.gameloft.com/iframe/?message=U2FsdGVkX19tOnrowdZsEefomJlsqCMXCeU0BUpxwHDUhU1LYfyOKlBwAitr%2BnoSvK88N3Q4UAUpyrjvMGWFzXTNRkEeFwSt5n%2BwGp7Zu%2Fw%3D',
        )

    @task
    def get_url_1(self):
        self.client.get(
            url='/ucdn/3402/000628.425ecea5cdea7570c8f7339ee9871cf1.css/url',
            headers=self.headers
        )

    @task
    def get_url_2(self):
        self.client.get(
            url='/ucdn/3402/loader.html/url',
            headers=self.headers
        )

    @task
    def get_url_3(self):
        self.client.get(
            url='/ucdn/3402/000628.ff1f5e01da24ce49d0d48488c7efaa87.otf/url',
            headers=self.headers
        )

    @task
    def get_url_4(self):
        self.client.get(
            url='/ucdn/3402/000628.fcb0078c0bbef4e1f3026d526f5667db.png/url',
            headers=self.headers
        )

    @task
    def get_url_5(self):
        self.client.get(
            url='/ucdn/3402/000628.b3ee7b1f96bba39e1fb1fff47fd54ef4.jpg/url',
            headers=self.headers
        )

    @task
    def get_url_6(self):
        self.client.get(
            url='/ucdn/3402/000628.298c83b8e89d7028acb4fc4643ad2375.m4a/url',
            headers=self.headers
        )

    @task
    def get_static_1(self):
        self.client.get(
            url='https://iris07-gold-ssl-gzip.gameloft.com/3402/000628.414c1b406fca3379e24775508287aaf7_1572937056.48.png',
            headers=self.headers2
        )

    @task
    def get_static_2(self):
        self.client.get(
            url='https://iris07-gold-ssl-gzip.gameloft.com/3402/000628.49bd5f80e37288c5b8e966b849bba4d4_1572937054.44.jpg',
            headers=self.headers2
        )

    @task
    def get_static_3(self):
        self.client.get(
            url='https://iris07-gold-ssl-gzip.gameloft.com/3402/000628.2e140daf577667a44677dddb1ab8c128_1572937055.89.m4a',
            headers=self.headers2
        )

    @task
    def get_static_4(self):
        self.client.get(
            url='https://iris07-gold-ssl-gzip.gameloft.com/3402/000628.298c83b8e89d7028acb4fc4643ad2375_1572937056.82.m4a',
            headers=self.headers2
        )

    @task
    def get_static_5(self):
        self.client.get(
            url='https://iris07-gold-ssl-gzip.gameloft.com/3402/000628.ab93e044a9f8fe132160db30f4c1f7a5_1572937053.78.m4a',
            headers=self.headers2
        )

    @task
    def post_tracking(self):
        payload = {
            "ggi": 79403,
            "entity_type": "GAMELOFT_MINIGAME_BETA",
            "entity_id": "3402:79403:55:HTML5:Ads",
            "proto_ver": "55",
            "events": [{
               "gdid":0,
               "type":200116,
               "token":3,
               "data": {
                  "action_type":362818,
                  "ad":"mobile_browser",
                  "anon_id":"anonymous:3b8caef86f0bb7888ac6dba6cec6b8fa",
                  "campaign_id":1111,
                  "creative_id":"0",
                  "custom_tracking":"N/A",
                  "d_country":"",
                  "ip_country":"",
                  "score":0,
                  "source_game":0,
                  "game_igp_code":"N/A",
                  "time_spent_loading":1511,
                  "total_time_spent_ads":0,
                  "total_time_spent_playing":0,
                  "ver":"55",
                  "iv_location_type":"IV",
                  "rim_pointcut_id":"N/A"
               }
            }]
        }
        self.client.post(
            url='https://oms.gameloft.com/api/pub/tracking',
            json=payload,
            headers=self.headers3
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
