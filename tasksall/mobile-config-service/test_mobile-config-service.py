from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    headers = {
        "X-Shopback-Build": "2310000",
        "X-Shopback-Agent": "sbiosagent",
        "X-Shopback-Store-Service": "true",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Domain": "www.shopback.sg"
    }

    @task(1)
    def get_configurations(self):
        self.client.get("/v2/mobile/services/configurations", headers=self.headers)


class AppUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
