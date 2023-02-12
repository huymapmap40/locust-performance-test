from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
  def __init__(self, parent):
    super(UserBehavior, self).__init__(parent)

  @task(8)
  def getNavDefault(self):
    self.client.get(
      url='/v1/navigations?live=1&limit=5&type=default',
    )

  @task(1)
  def getNavRaf(self):
    self.client.get(
      url='/v1/navigations?live=1&limit=5&type=raf',
    )

  @task(1)
  def getCountryConfig(self):
    self.client.get(
      url='/countries/sg',
    )

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  wait_time = between(0.1, 0.5)
