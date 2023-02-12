from typing import Dict
from locust import TaskSet, HttpUser, task, between
from utility_users import get_unique_account_id, get_user_headers_by_account_id

class UserBehaviour(TaskSet):
    account_id = 0

    def on_start(self) -> None:
        self.account_id = get_unique_account_id()

    @task
    def check_new_user(self) -> None:
        with self.client.get(
            url="/graphql",
            params={'query': f'{{user(accountId:{self.account_id}){{isSbgoNewCustomer isSbocNewCustomer isNewCustomer}}}}'}
        ) as res:
            res.close()


class EcommerceUser(HttpUser):
    wait_time = between(3, 10)
    tasks = [UserBehaviour]
