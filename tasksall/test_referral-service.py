import random
from locust import HttpUser, task, between

# staging-sg
# user_ids = [18900,23493,48181,66245,181949,3809184,3821885,4290515,4351014,4649981,4688453,4919549,5094034,5196566,5196619,5196665]

# staging-th
user_ids = [1,2,3,4,5,6,7,8,9,10]

class User(HttpUser):
    wait_time = between(4, 10)
    account_id = 0

    def on_start(self):
        self.account_id = random.choice(user_ids)

    @task
    def get_code(self) -> None:
        self.client.get(url=f"/referral/account/{self.account_id}/code", name="/referral/account/:accountId/code")

    @task
    def get_progress(self) -> None:
        self.client.get(url=f"/referral/account/{self.account_id}/progress", name="/referral/account/:accountId/progress")
