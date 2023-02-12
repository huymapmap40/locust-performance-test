from locust import HttpLocust, TaskSet, task, TaskSequence, seq_task, between
from random import choice
import json, logging, sys, base64, datetime

class UserBehavior(TaskSequence):
    # Populate with random data
    def on_start(self):
    
      self.possibleTypesList = [
        "malaysia",
        "voucher",
        "data",
        "game",
        "etoll",
        "pulsa",
        "indonesia"
      ]

      self.possibleCodeList = [
        "alfamart5",
        "ancolengate",
        "aovvoucher18",
        "celcom10",
        "celcom15",
        "celcom100",
        "celcom20",
        "ctcorp50",
        "dana10",
        "dana100",
        "dana150",
        "dana25",
        "haxis10000",
        "haxis100000",
        "haxis15000",
        "haxis200000",
        "haxis25000",
        "haxis50000",
        "hbattlenet10",
        "hbattlenet20",
        "hbattlenet5",
        "cc161",
        "cccantik",
        "cceallkor",
        "cceg"
      ]

    #GET /get/pricelist
    @task(1)
    def get_pricelist(self):
      pricelistEndpoint = "/pricelist/" + choice(self.possibleTypesList) + "/" +  choice(self.possibleCodeList)
      with self.client.get(
        pricelistEndpoint, 
        catch_response=True
      ) as response:
          if response.status_code == 200 or response.status_code == 404:
            response.success()
      logging.info("GET pricelist")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 10)
