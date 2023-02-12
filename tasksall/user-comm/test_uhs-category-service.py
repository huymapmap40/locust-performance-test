from locust import HttpUser, TaskSet, task, between
import random
import json

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'AccountId': random.randint(1, 20000),
            'Uuid': random.randint(1, 20000),
        }

    def isSuccess(self, response):
            if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
                response.success()
            if response.status_code == 500 or response.status_code == 503:
                body = response.json()
                logging.info('fail" %s ', body['error']['message'])
                logging.info('fail" %s ', body['error']['code'])

    @task
    def getMlCategories(self):
        with self.client.get(url="/v2/universal-categories?lang=en&queryType=recommendation",
                                      headers=self.headers, catch_response=True) as response:
             self.isSuccess(response)
        self.client.close()

#     @task
#     def getCategories(self):
#         with self.client.get(url="/v1/universal-categories?lang=en&queryType=manual",
#                                       headers=self.headers, catch_response=True) as response:
#              self.isSuccess(response)
#         self.client.close()

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(1, 1)
