from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):

  def __init__(self, parent):
    super(UserBehavior, self).__init__(parent)

    self.headers = {
      'Authorization': 'Bearer eyJpZCI6IDUyNDgzfQ==',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbconsumeragent/1.0'
    }
    self.agents = ['sbconsumeragent/1.0', 'sbmwebagent/1.0', 'sbiosagent/1.0', 'sbandroidagent/1.0']
    self.payload = {
      'browserName': 'Chrome',
      'browserVersion': '76.0.3809.100',
      'browserPlatform': 'Apple Mac',
      'referrerUrl': 'https://www.goshopback.vn/',
      'advertisingId': '78ccb948',
      'appsflyerId': '1234',
      'platformTrackingId': '1234'
    }
    self.merchantIds = [19312,19352,19318,19354,18684,19293,18133]
    self.affiliateLinkIds = [99520, 99521, 308428, 308429, 63238, 71299]
    self.dealIds = [116451,144194,143252,139574,138002]
    self.couponIds = [13529,13530]


  @task(1)
  def merchantRedirect(self):
    merchantId = random.choice(self.merchantIds)
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.client.post(
      url='/v1/redirect?type=merchant&id=' + str(merchantId),
      headers=self.headers,
      json=self.payload
    )

  @task(1)
  def productRedirect(self):
    affiliateLinkId = random.choice(self.affiliateLinkIds)
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.client.post(
      url='/v1/redirect?type=product&id=' + str(affiliateLinkId),
      headers=self.headers,
      json=self.payload
    )

  @task(1)
  def dealRedirect(self):
    dealId = random.choice(self.dealIds)
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.client.post(
      url='/v1/redirect?type=deal&id=' + str(dealId),
      headers=self.headers,
      json=self.payload
    )

  @task(1)
  def couponRedirect(self):
    couponId = random.choice(self.couponIds)
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.client.post(
      url='/v1/redirect?type=coupon&id=' + str(couponId),
      headers=self.headers,
      json=self.payload
    )

  @task(1)
  def affiliateLinkRedirect(self):
    affiliateLinkId = random.choice(self.affiliateLinkIds)
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.client.post(
      url='/v1/redirect?type=affiliate_link&id=' + str(affiliateLinkId),
      headers=self.headers,
      json=self.payload
    )


class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  wait_time = between(5, 10)
