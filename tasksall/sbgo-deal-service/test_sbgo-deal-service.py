import time
import random
import json
from locust import HttpUser, task, between
from users_utility import get_user_headers_by_account_id
from account_ids import all_user_ids
from locations import all_locations

class User(HttpUser):
    wait_time = between(1, 3)
    account_id = 0
    location = None
    headers = {}

    def on_start(self):
        self.account_id = random.choice(all_user_ids)
        self.location = random.choice(all_locations)
        self.headers = get_user_headers_by_account_id(self.account_id)

    @task(1)
    def get_in_store_deals_near_you(self):
        data = {
          "tags": ["sbgo-deal-group-all"],
          "location": self.location,
        }
        pagination_prob = 0.1
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Location/all-deals)")

        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/sbgo-deal-service/deals/search (Location/all-deals)")
    
    @task(1)
    def get_top_deals_near_you(self):
        data = {
          "tags": ["sbgo-v3-top-brands-universal-sorting"],
          "location": self.location,
        }
        pagination_prob = 0.1
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Location/top-deals)")

        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/sbgo-deal-service/deals/search (Location/top-deals)")

    @task(1)
    def get_manually_sorted_deals(self):
        data = {
          "sort": {
            "type": "manual",
            "setKey": "sbgo-v3-top-brands-universal-sorting-retail"
          }
        }
        pagination_prob = 0.1
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Manual)")

        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/sbgo-deal-service/deals/search (Manual)")

    @task(1)
    def get_recommended_in_store_deals(self):
        data = {
          "mlKey": "recommended",
        }
        pagination_prob = 0.1
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Location/all-deals)")

        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/sbgo-deal-service/deals/search (mlKey/recommended)")

    @task(1)
    def get_recommended_online_vouchers(self):
        data = {
          "mlKey": "oc:recommended",
        }
        pagination_prob = 0.1
        res = self.client.post(url="/sbgo-deal-service/deals/search", headers=self.headers, json=data, name="/sbgo-deal-service/deals/search (Location/all-deals)")

        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/sbgo-deal-service/deals/search (mlKey/oc:recommended)")
