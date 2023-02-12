from locust import HttpUser, TaskSequence, seq_task
import base64
import random


class UserBehavior(TaskSequence):

    def on_start(self):

        self.headers = {"X-Shopback-Build": "2000599",
                        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
                        "X-Shopback-Language": "en",
                        "X-Shopback-Agent": "sbandroidagent/2.0.5",
                        "X-Shopback-Domain": "www.shopback.sg"}

    @seq_task(1)
    def spam(self):

        cacheValue = "no-cache" if random.randint(0, 1) == 0 else "cache"
        self.headers.update({"Cache-Control": cacheValue})

        print("Spamming partner-apps with "+cacheValue)
        response = self.client.get(
            "/mobile/partner-apps", headers=self.headers)
        print(response.text)


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 300
    max_wait = 800
