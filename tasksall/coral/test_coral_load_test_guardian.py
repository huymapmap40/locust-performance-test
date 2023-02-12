import uuid
import random
from locust import HttpUser, TaskSet, task, between

def get_test_list(self):
  test_list = []
  with self.client.get('/block-agents') as response:
    json_response_array = response.json()
    for agent in json_response_array:
      test_list.append(agent['name']) # append existed agent
      test_list.append(str(uuid.uuid4())) # append random UUID
  return test_list

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.test_list = get_test_list(self)

    def check_get_block_agent(self, response):
      if response.status_code == 200:
        response.success()
      elif response.status_code == 404:
        response.success()

    @task
    def get_block_agent(self):
      sample_uuid = random.sample(self.test_list, 1)
      url = '/block-agents/{}'
      with (
        self.client.get(
          url.format(sample_uuid[0]),
          name=url,
          catch_response=True
        )
      ) as response:
        self.check_get_block_agent(response) 

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0, 1)
