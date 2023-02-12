from locust import HttpUser, TaskSet
import os

SHOPBACK_API_KEY_SECRET_CONSUMER = os.getenv('SHOPBACK_API_KEY_SECRET_CONSUMER')

def healthCheck(l):
    l.client.get("/health")

def bucketService(l):
    l.client.post("/link/validate", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"secret"})

def categoryService(l):
    endpoint = "/categories/50000989"
    l.client.get(endpoint, headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"secret"})

def mockService_r200_d100(l):
    endpoint = "/mock/loadtest?test=200&delay=100"
    l.client.get(endpoint, headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":SHOPBACK_API_KEY_SECRET_CONSUMER, "Connection":"close"})
    # l.client.close()

def versionCheck(l):
    endpoint = "/version?ilove=shopback-0-0-1"
    l.client.get(endpoint, headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"secret"})

class UserBehavior(TaskSet):
    # tasks = {healthCheck:1, bucketService:1}
    # tasks = {healthCheck:1}
    # tasks = {categoryService:1}
    # tasks = {versionCheck:1}
    tasks = {mockService_r200_d100:1}

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000