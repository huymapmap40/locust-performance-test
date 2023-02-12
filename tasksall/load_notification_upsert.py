# locust -f orca-rs-load-test.py

from locust import HttpLocust, TaskSet

offer_list = [
    '636fa4cbe8b9e9bb3b172e14a998660382931777',
    '86d9f8b919f8fb7dee1c018e3dca838083e8e067',
    'e80e42158b9306f1cfa9d5a99ea0369e88bac6e4',
    '6d98307fe425679dff3a110862c301463e762815'
]


def redirect_test(l):
    for i in offer_list:
        endpoint = '/product/redirect/'+i
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "JWT eyJ1dWlkIjoiODI3YWE5ZDM4ZTRmNDYwOGFjNjA5ZDZjNDEzMzJkYzIiLCJpc3MiOiJ3d3cuc2hvcGJhY2sucGgiLCJpc3N1ZWRBdCI6MTU5NTU3NDkzNS42MDQsImlhdCI6MTU5NTU3NDkzNSwiZXhwIjoxNTk1NjYxMzM1LCJpZCI6MjQ2NDA1MX0=",
            "X-Shopback-Country": "TW",
            "x-shopback-domain": "www.shopback.com.tw",
            "X-Shopback-Agent": "sbiosagent/1.0",
            "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
            "X-Shopback-Language": "zh",
            "X-Shopback-Store-Service": "true"
        }
        payload = {
            "browser_name": "Chrome",
            "browser_platform": "Android",
            "browser_version": "71.0.3578.98",
            "ip_address": "202.39.237.203, 162.158.6.159, 70.50.55.234",
            "device_id": "test",
            "referrer_url": "localhost:3000"
        }
        print('Calling redirect enpoint: %s', % (endpoint))
        l.client.post(endpoint, json=(payload),
                      headers=headers, catch_response=False)


class MatchAllSet(TaskSet):
    tasks = {redirect_test: 1}


class WebsiteUser(HttpLocust):
    task_set = MatchAllSet
    min_wait = 1000
    max_wait = 2000
