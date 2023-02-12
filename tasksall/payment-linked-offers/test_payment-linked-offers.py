import time
import random
import json
from locust import HttpUser, task, between
from users_utility import get_user_headers_by_account_id
from top_outlet_ids import outlet_ids
from account_ids import all_user_ids

class User(HttpUser):
    wait_time = between(1, 3)
    account_id = 0
    headers = {}

    def on_start(self):
        self.account_id = random.choice(all_user_ids)
        self.headers = get_user_headers_by_account_id(self.account_id)

    @task(13)
    def get_payment_methods(self) -> None:
        self.client.get(
            url="/plo/paymentmethods",
            headers=self.headers,
        )

    @task(8)
    def get_mobile_configurations(self) -> None:
        self.client.get(
            url="/plo/mobile/configurations?coordinates=1.2770321,103.8458774",
            headers=self.headers,
            name="/plo/mobile/configurations",
        )

    @task(5) # also includes weightage for /plo/universal-search/outlets
    def outlets_search(self) -> None:
        data = {
            "filters": [],
            "sort": {
                "type": "distance",
                "order": "asc",
                "metadata": {
                    "lat": 1.2770321,
                    "lon": 103.8458774
                }
            },
            "limit": 1
        }
        pagination_prob = 0.1
        res = self.client.post(
            url="/plo/mobile/filter/outlets",
            headers=self.headers,
            json=data,
        )
        if res.status_code == 200:
          data = json.loads(res.text)
          next_page_url = data["meta"]["pagination"]["next"]
          if next_page_url is not None and random.random() < pagination_prob :
            next_page_url = "/{}".format(next_page_url)
            self.client.get(url=next_page_url, headers=self.headers, name="/plo/mobile/filter/outlets")

    @task(1)
    def get_outlet(self) -> None:
        outlet_id = random.choice(outlet_ids)
        self.client.get(url=f"/plo/outlet/{outlet_id}", headers=self.headers, name="/plo/outlet/:id")
