from locust import HttpUser, TaskSet

def healthCheck(l):
    l.client.get("/health")
    # l.client.get("/oauth/refresh_token")

# def bucketService(l):
#     l.client.post("/link/validate", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})


class UserBehavior(TaskSet):
    # tasks = {healthCheck:1, bucketService:1}
    tasks = {healthCheck:1}

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000