from locust import HttpLocust, TaskSet, task, TaskSequence, seq_task, between
from random import randint
import json, logging, sys, base64, datetime

sessionsEndpoint = "/v2/sessions"
healthEndpoint = "/health"

headers = {
  "Accept":"*/*", 
  "Accept-Encoding":"gzip, deflate",
  "Cache-Control":"no-cache",
  "Connection":"keep-alive",
  "Host":"1.50.44.112",
  "Postman-Token":"a2ba7f3f-db78-465e-a439-35c5c7850088de1e3468-386d-46da-abb3-0e18ad5a51ba",
  "User-Agent":"PostmanRuntime/7.15.2",
  "X-Shopback-Agent":"sbmobileagent",
  "X-Shopback-Key":"q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
  "cache-control":"no-cache",
  "Content-Type":"application/json"
}

class UserBehavior(TaskSequence):
    # Populate with random data
    def on_start(self):
        
        self.trackingId = randint(1,9999999)
        self.platformTrackingId = randint(1,9999999)
        self.metaData = {
            "appsflyerId": randint(1,99999),
            "shoppingtripId": randint(1,99999),
            "shoppingtripUuid": randint(1,9999999),
            "createdAt": "2017-01-01T03:54:52 -08:00",
            "userAgent": "android",
            "domain": "www.shopback.sg"
        }

    #POST /v2/sessions
    @task(1)
    def post_sessions(self):
        self.client.post(
            sessionsEndpoint,
            data = json.dumps({
                "trackingId": self.trackingId,
	            "platformTrackingId": self.platformTrackingId,
                "metaData": self.metaData
            }),
            headers = headers,
            name = "Post sessions"
        )
        
        data = json.dumps({
                "trackingId": self.trackingId,
	            "platformTrackingId": self.platformTrackingId,
                "metaData": self.metaData
            })
        
        logging.info(data)
        
        logging.info("POST to create new sessions")

    @task(0)
    def get_health(self):
        self.client.get(healthEndpoint)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 10)
