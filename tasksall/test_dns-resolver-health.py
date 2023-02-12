from locust import HttpUser, TaskSet

def healthCheck(l):
    l.client.get("/?hostname=example.com")

class UserBehavior(TaskSet):
    # tasks = {healthCheck:1, bucketService:1}
    tasks = {healthCheck:1}

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 0
    max_wait = 1000