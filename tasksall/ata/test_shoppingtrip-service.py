from locust import HttpUser, TaskSet, task, between
import random
import json

class UserBehavior(TaskSet):

  def __init__(self, parent):
    super(UserBehavior, self).__init__(parent)


  @task(5)
  def shoppingtripDetail(self):
    shoppingtripIds = [69116515, 69116512, 69116509, '707faae2663944bf86759cadb3bbadaa', '40860d565c844e518a031072bcce5e9b', 'fcecb2aa815f47f9a0bc38c4787b29ba']
    shoppingtripId = random.choice(shoppingtripIds)
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.client.get(
      url='/v2/shoppingtrips/' + str(shoppingtripId),
      headers=headers
    )

  @task(5)
  def internalShoppingtripDetail(self):
    shoppingtripIds = [69116515, 69116512, 69116509, '707faae2663944bf86759cadb3bbadaa', '40860d565c844e518a031072bcce5e9b', 'fcecb2aa815f47f9a0bc38c4787b29ba']
    shoppingtripId = random.choice(shoppingtripIds)
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.client.get(
      url='/v1/internal/shoppingtrips/' + str(shoppingtripId),
      headers=headers
    )

  @task(1)
  def shoppingtripsV3(self):
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    page = random.randint(1, 5)
    self.client.get(
      url='/v3/shoppingtrips?pageSize=10&page=' + str(page),
      headers=headers
    )

  @task(1)
  def availableMerchants(self):
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.client.get(
      url='/v3/shoppingtrips/available-merchants',
      headers=headers
    )
  
  @task(1)
  def availableStatuses(self):
    headers = {
      'Authorization': 'Bearer eyJpZCI6IDI4OTQ4MH0=',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.client.get(
      url='/v3/shoppingtrips/available-statuses',
      headers=headers
    )


class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  wait_time = between(5, 10)
