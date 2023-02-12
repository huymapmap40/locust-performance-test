from locust import HttpUser, TaskSet, task
import random
import uuid
from used_shoppingtrip_ids import *
class UserBehavior(TaskSet):
    def getShoppingtripId(self):
        return str(uuid.uuid4())
        
    @task
    def createSessionAfterRedirect(self):
        shoppingtripId = self.getShoppingtripId()
        trackingId = str(uuid.uuid4())
        payload = {
            'trackingId': shoppingtripId,
            'platformTrackingId': trackingId,
            'metaData': {
              'appsflyerId': trackingId,
              "shoppingtripId": shoppingtripId,
              "userAgent": random.choice(['ios', 'android']),
              "domain": 'www.shopback.sg'
            }
        }

        self.client.post(
          url='/v2/sessions',
          json=payload
        )

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
