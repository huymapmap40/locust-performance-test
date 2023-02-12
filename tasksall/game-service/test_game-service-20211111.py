import base64
import json
import time
from datetime import datetime, timedelta
from hashlib import sha1
from random import randint

from locust import HttpUser, TaskSet, between, task

game_service_base_url = 'http://game-service'
prize_generator_service_base_url = 'http://prize-generator-service'

to_date = datetime.now()
from_date = to_date - timedelta(days=1)

tour_id = '616e3822ec7ba3101ec96d9d'


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.account_id = 100000000 + randint(1, 200)

        access_token = 'JWT ' + self.generate_jwt_token()
        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'Authorization': access_token
        }

    @staticmethod
    def gen_hash_string(random_string, game_id, cdata, gdata, grdata):
        idx = int(len(random_string) / 3)
        test_string = '{}{}'.format(random_string[0:idx], random_string[idx + 1:len(random_string)])
        data_string = '{}{}{}{}'.format(game_id, cdata, gdata, grdata)
        messageDigest = sha1()
        messageDigest.update(bytes('{}{}{}'.format(test_string, data_string, test_string), encoding='utf-8'))
        hashed = messageDigest.digest()
        return base64.b64encode(hashed)

    def generate_jwt_token(self):
        json_obj = {
            'uuid': '0c4fbbc97da24b52a81ffe0da4c86acf',
            'iss': 'iOS',
            'issuedAt': 1635848816,
            'iat': 1635848816,
            'exp': 1655848816,
            'id': self.account_id
        }

        encoded_token = json.JSONEncoder().encode(json_obj)
        encoded_auth = base64.b64encode(encoded_token.encode("utf-8"))

        # access_token = str(encoded_auth).encode('utf-8')
        access_token = str(encoded_auth, 'utf-8')

        return access_token

    @task(200)
    def get_profile(self):
        self.client.get(
            url="{game_service_base_url}/game/v1/profiles/{accountId}".format(
                game_service_base_url=game_service_base_url, accountId=self.account_id),
            headers=self.headers
        )

    @task(200)
    def get_tournaments(self):
        self.client.get(
            url="{game_service_base_url}/game/v1/troopers/tournaments/active".format(
                game_service_base_url=game_service_base_url),
            headers=self.headers
        )

    @task(200)
    def get_tournament_prize(self):
        self.client.get(
            url="{game_service_base_url}/game/v1/troopers/tournaments/current-prize".format(
                game_service_base_url=game_service_base_url),
            headers=self.headers
        )

    @task(200)
    def get_history_prizes(self):
        self.client.get(
            url='{game_service_base_url}/game/v1/troopers/history-prizes/{accountId}?limit=5'.format(
                game_service_base_url=game_service_base_url, accountId=self.account_id),
            headers=self.headers
        )

    @task(200)
    def get_history_boards(self):
        self.client.get(
            url='{game_service_base_url}/game/v1/troopers/history-boards/{accountId}?limit=5'.format(
                game_service_base_url=game_service_base_url, accountId=self.account_id),
            headers=self.headers
        )

    @task(200)
    def get_leader_boards(self):
        self.client.get(
            url='{game_service_base_url}/game/v1/troopers/leaderboard/{accountId}?limit=10&tourId={tour_id}&fromDate={from_date}&toDate={to_date}'.format(
                game_service_base_url=game_service_base_url, accountId=self.account_id, tour_id=tour_id, 
                from_date=from_date.isoformat(), to_date=to_date.isoformat()),
            headers=self.headers
        )

    @task(200)
    def get_history_prizes(self):
        self.client.get(
            url='{game_service_base_url}/game/v1/troopers/history-prizes/{accountId}?limit=5'.format(
                game_service_base_url=game_service_base_url, accountId=self.account_id),
            headers=self.headers
        )

    @task(20)
    def get_prize_categories(self):
        self.client.get(
            url='{prize_generator_service_base_url}/games/v1/prizes/categories'.format(
                prize_generator_service_base_url=prize_generator_service_base_url), headers=self.headers
        )

    @task(20)
    def play_and_end(self):
        self.get_profile()
        payload = {"accountName": "load-test ", "gameId": "troopers"}

        play_response = self.client.post(
            url='{game_service_base_url}/game/v1/troopers/play/{accountId}'.format(
                game_service_base_url=game_service_base_url, accountId=self.account_id),
            headers=self.headers,
            json=payload
        )
        print('play_response: {}'.format(play_response.text))

        if play_response:
            res = play_response.json()
            cdata = res['data']['cdata']
        else:
            return

        # config = decrypt(cdata, GAME_ID)
        # specialScoreMultiplier = config[40:43]
        # scoreMultiplier= 50

        payload = {
            "gameId": 'troopers',
            "cdata": cdata,
            "gdata": "U2FsdGVkX19SyNUnXf90di3oMvF9hF6HUfTePC9g0qyfv4PrXND6ZKlEkGN08L1E",
            "grdata": "U2FsdGVkX19xIawUy21I8x4bYa0gtH5D03iZIlm5HJcDh0INb1Bgj1V6I6F/DUVy"
        }
        time.sleep(5)
        headers = self.headers

        headers['x-random-string'] = 'U2FsdGVkX183R'
        headers['x-hash'] = self.gen_hash_string(headers['x-random-string'], 'troopers',
                                                      payload['cdata'], payload['gdata'], payload['grdata'])
        
        play_response_end = self.client.post(
            url='{game_service_base_url}/game/v1/gl/end'.format(game_service_base_url=game_service_base_url),
            headers=headers,
            json=payload
        )

        print('Payload: {} Response: {}'.format(json.dumps(payload), play_response_end.text))


class Player(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.3, 2)
