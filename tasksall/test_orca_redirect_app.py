import csv, random
from locust import HttpLocust, TaskSet

def readCSV(fileName):
    with open(fileName, 'r') as f:
        r = csv.reader(f, delimiter=',')
        # next(r)  # skip header line
        return list(r)

API_GATEWAY = "http://gateway-staging.shopback.com.tw"

# Login variable
EMAIL = "andy.li@shopback.com"  # 2464051
PASSWORD = "abcd1234"
COUNTRY = "TW"
DOMAIN = "www.shopback.com.tw"

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": USE_IRON_GATE,
    "X-Shopback-Country": COUNTRY,
    "x-Shopback-domain": DOMAIN,
    "x-shopback-recaptcha-type": "bypass"
}

def login(email, password):
    url = "{}/members/sign-in".format(API_GATEWAY)
    payload = json.dumps({
        "email": email,
        "password": password,
        "client_user_agent": "test"
    })
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    if response.status_code == 200:
        if 'auth' in response.json():
            return response.json()['auth']['access_token']
    print('Cant to get token {}'.format(response.json()))
    exit(1)


offerIds = readCSV("offerIds.csv")
userAgents = [
    {
        "X-Shopback-Agent": "sbiosagent",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"
    },
    {
        "X-Shopback-Agent": "sbandroidagent",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"
    }
]



def redirect_test(l):
  offerId = random.choice(offerIds)
  userAgent = random.choice(userAgents)
  endpoint = '/product/redirect/v2/'+offerId[0]
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "JWT eyJ1dWlkIjoiODI3YWE5ZDM4ZTRmNDYwOGFjNjA5ZDZjNDEzMzJkYzIiLCJpc3MiOiJ3d3cuc2hvcGJhY2suY29tLnR3IiwiaXNzdWVkQXQiOjE1OTU1NzU0ODAuNjQsImlhdCI6MTU5NTU3NTQ4MCwiZXhwIjoxNTk1NjYxODgwLCJpZCI6MjQ2NDA1MX0=",
      "X-Shopback-Country": "TW",
      "x-shopback-domain": "www.shopback.com.tw",
      "X-Shopback-Language": "zh",
      "X-Shopback-Store-Service": "true"
  }
  headers.update(userAgent)
  payload = {
      "browser_name": "Chrome",
      "browser_platform": "Android",
      "browser_version": "71.0.3578.98",
      "ip_address": "202.39.237.203, 162.158.6.159, 70.50.55.234",
      "device_id": "test",
      "referrer_url": "localhost:3000"
  }
  l.client.post(endpoint, json=(payload),name="app redirect v2", headers=headers, catch_response=False)


class MatchAllSet(TaskSet):
    tasks = {redirect_test: 1}


class WebsiteUser(HttpLocust):
    task_set = MatchAllSet
    min_wait = 1000
    max_wait = 2000
