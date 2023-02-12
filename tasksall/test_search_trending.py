import random
import sys
from locust import HttpLocust, TaskSet

userAgents = [
    {
        "X-Shopback-Agent": "sbiosagent",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"
    },
    {
        "X-Shopback-Agent": "sbandroidagent",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"
    },
    {
        "X-Shopback-Agent": "sbmwebagent",
        "X-Shopback-Key": "824fe3aecc3o9xnaf756690fd8d4ec58"
    },
    {
        "X-Shopback-Agent": "sbconsumeragent",
        "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210"
    },
]


def search_trending(l):
    headers = random.choice(userAgents)
    url = "/search/keyword/trend"
    l.client.get(url, headers=headers, name="/search/keyword/trend")


class UserBehavior(TaskSet):
    tasks = {search_trending: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
