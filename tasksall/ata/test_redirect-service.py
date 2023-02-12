from locust import HttpUser, TaskSet, task, between
import random
import json

class UserBehavior(TaskSet):

  def __init__(self, parent):
    super(UserBehavior, self).__init__(parent)

    self.headers = {
      'Authorization': 'Bearer eyJpZCI6IDM4MDkxODR9',
      'Content-Type': 'application/json',
      'X-Shopback-Agent': 'sbiosagent/1.0'
    }
    self.agents = ['sbiosagent/1.0', 'sbandroidagent/1.0']
    self.payload = {
      'browserName': 'Chrome',
      'browserVersion': '76.0.3809.100',
      'browserPlatform': 'Apple Mac',
      'referrerUrl': 'https://www.shopback.sg/',
      'advertisingId': '78ccb948',
      'appsflyerId': '1234',
      'platformTrackingId': '8AD1DF66-0E5C-4C4C-A5C8-56085AB8DA3A',
      'appsflyerId': '1672026221153-8166054',
      'experimentSource': 'sboc_redirect_deeplink'
    }
    self.redirectLinks = [
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cf4',
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cf3',
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cf2',
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cf1',
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cf0',
      'www.shopback.sg/sboc/redirects/63a5965d2ef52b3ab8817cef',
      'www.shopback.sg/sboc/redirects/63a596562ef52b3ab8817ced',
      'www.shopback.sg/sboc/redirects/63a596562ef52b3ab8817cec',
      'www.shopback.sg/sboc/redirects/63a596562ef52b3ab8817ceb',
      'www.shopback.sg/redirect/alink/76488',
      'www.shopback.sg/redirect/alink/117518',
      'www.shopback.sg/redirect/alink/120446',
      'www.shopback.sg/redirect/alink/296643',
      'www.shopback.sg/redirect/alink/296642',
      'www.shopback.sg/redirect/alink/222309',
      'www.shopback.sg/redirect/alink/118213'
    ]

  @task(1)
  def sbocRedirect(self):
    self.headers['X-Shopback-Agent'] = random.choice(self.agents)
    self.payload['redirectLink'] = random.choice(self.redirectLinks)
    self.client.post(
      url='/v1/sboc/redirects',
      headers=self.headers,
      json=self.payload
    )


class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  wait_time = between(5, 10)
