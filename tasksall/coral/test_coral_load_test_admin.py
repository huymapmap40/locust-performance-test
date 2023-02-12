import json
import os
import sys
import random
from locust import HttpUser, task, between

with open(os.path.join(sys.path[0], 'config.json')) as f:
  data = json.load(f)

##########################################################
## Make sure you select the right environment variables ##
##########################################################
env_vars = data['ENV_VARS']['STG-TW']
##########################################################

# ShopBack internal clients (other ShopBack teams)
class InternalClient(HttpUser):
  wait_time = between(0.1, 0.3)

  def on_start(self):
    self.client.headers = {
      'Content-Type': 'application/json',
      'X-Shopback-Domain': env_vars['domain'],
      'X-Shopback-Agent': 'sbconsumeragent/1.0',
      'X-Shopback-Member-Operator': 'cashback-engine-service'
    }

  def random_account_id(self):
    # the old_ids of 1111load+test{id}@shopback.com accounts
    return random.randint(env_vars['accounts']['min_old_id'], env_vars['accounts']['max_old_id'])

  def check_get_account_response(self, response):
    # because some old_ids in the range above are empty
    # (The range contains 16,173 numbers but there are only 15k accounts)
    # the error code 50002 (user id not found) is also an correct response
    if response.status_code == 200:
      # success
      response.success()
    elif response.status_code == 404:
      body = response.json()
      if body['error']['code'] == 50002:
        # user not found
        response.success()

  @task
  def get_account_by_id(self):
    account_id = self.random_account_id()
    url = '/admin/{id}'
    with self.client.get(
      url.format(id=account_id) + '?operator=coral.loadtest@shopback.com',
      name=url,
      catch_response=True
    ) as response:
      self.check_get_account_response(response)



