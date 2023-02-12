from locust import HttpUser, TaskSet, task

class WebUserTaskSet(TaskSet):
    @task
    def apiStoresWithConfirmUrl(l):
        l.client.get("http://api.shopback.co.id/api/stores?metadata=confirmation-urls,cashback-disable-reasons,store-meta-info", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})
    
    @task
    def apiStoresWithName(l):
        l.client.get("https://www.shopback.co.id/api/store?fields=name,shortname", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})
    
    @task
    def shopfest(l):
        l.client.get("https://www.shopback.co.id/shopfest-1010", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})
    
    @task
    def homepage(l):
        l.client.get("https://www.shopback.co.id/", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})
    
    #@task
    #def mweb(l):
    #    l.client.get("https://m.shopback.co.id/api/mweb/v1/stores?top=true", headers={"X-Shopback-Agent":"sbconsumeragent/1.0", "X-Shopback-Internal":"682a46b19b953306c9ee2e8deb0dc210"})

class WebUserLocust(HttpUser):
    tasks = [WebUserTaskSet]
    min_wait = 2000
    max_wait = 4000
