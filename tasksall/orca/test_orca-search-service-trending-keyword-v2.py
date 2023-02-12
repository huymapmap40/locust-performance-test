import csv, random
from locust import HttpLocust, TaskSet

def search(l):
    url = "/search/v2/keyword/trend"

    headers={"X-Shopback-Agent": "sbiosagent", "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"}
    l.client.get(url, headers=headers, name="/search/keyword/trend")


class UserBehavior(TaskSet):
     tasks = {search:1}

class WebsiteUser(HttpLocust):
        task_set = UserBehavior
        min_wait = 1000
        max_wait = 1000
