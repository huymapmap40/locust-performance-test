from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.client.verify = False
        self.slugs = [
            "/asos",
            "/booking-com",
            "/lazada",
            "/shopee",
            "/zalora-promo-code",
            "/agoda",
            "/dyson",
            "/trip-com-promo-code",
            "/taobao",
            "/fairprice-online",
        ]

    @task
    def requestMerchantPage(self):
        slug = random.choice(self.slugs)
        response = self.client.get(slug)

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(0.3, 0.8)

