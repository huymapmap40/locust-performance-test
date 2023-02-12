import time
import random
import json
from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(1, 3)
    location = None
    headers = {
        "X-Shopback-Agent": "sbandroidagent/1.0",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Build": "3200000",
    }

    @task(1)
    def get_manually_sorted_deals(self):
        data = {
          "sort": {
            "type": "manual",
            "setKey": "sbgo-activities-gb-deal-group"
          },
          "limit": 5
        }
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Manual)")
