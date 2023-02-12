import random, json, base64
from locust import HttpLocust, TaskSet

def generate_jwt_token(account_id):
    authorization_content = json.dumps({
        "uuid": "479c94048a8e410694ea24fc17302906",
        "iss": "www.shopback.com.tw",
        "issuedAt": 1577477107.184,
        "iat": 1577477107,
        "exp": 1578773107,
        "id": account_id
    })
    return base64.b64encode(authorization_content.encode('utf-8')).decode('utf-8')

account_id = [97, 88, 2464051, 78, 65, 1, 58, 14, 22, 90, 55]


def favorite_test(l):
  random_id = random.choice(account_id)
  access_token = 'JWT {}'.format(generate_jwt_token(random_id)) 
  headers = {
      "Content-Type": "application/json",
      "X-Shopback-Agent": "sbiosagent/1.0", 
      "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
      "X-Shopback-Store-Service": "true",
      "Authorization": access_token,
      "X-Shopback-Country": "TW",
      "x-shopback-domain": "www.shopback.com.tw",
      "X-Shopback-Language": "zh"
  }
  l.client.get("/favorite/product?page=1&includeGroup=true", headers=headers, name="/favorite/product")

class MatchAllSet(TaskSet):
    tasks = {favorite_test: 1}


class WebsiteUser(HttpLocust):
    task_set = MatchAllSet
    min_wait = 1000
    max_wait = 2000
