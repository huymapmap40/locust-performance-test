from locust import HttpUser, TaskSet, task, between
import random
import json

class UserBehavior(TaskSet):

  def __init__(self, parent):
    super(UserBehavior, self).__init__(parent)


  @task(1)
  def getConversionPatterns(self):
    headers = {
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.client.get(
      url='/conversion-patterns/merchants/12501',
      headers=headers
    )

  @task(1)
  def createPresignedUrl(self):
    shoppingtripIds = ['707faae2663944bf86759cadb3bbadaa', '40860d565c844e518a031072bcce5e9b', 'fcecb2aa815f47f9a0bc38c4787b29ba']
    shoppingtripId = random.choice(shoppingtripIds)
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    payload = {
      'url': 'https://checkout.iherb.com/transactions/checkout/orderreceipt/1234314555'
    }
    self.client.post(
      url='/v1/shoppingtrip-documents/' + shoppingtripId + '/url',
      headers=headers,
      json=payload
    )


class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  wait_time = between(5, 10)
