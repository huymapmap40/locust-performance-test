from locust import HttpUser, TaskSet, task, between
import random

headers = {
    'Content-Type': 'application/json'
}


class UserBehavior(TaskSet):
    page_ids = []

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def on_start(self):
        response = self.client.get(
            url='/int/pages',
            headers=headers)
        self.page_ids = [page['_id'] for page in response.json()['data']]

    @task(25)
    def get_pages(self):
        self.client.get(url='/int/pages')

    @task(1)
    def get_page_by_id(self):
        page_id = random.choice(self.page_ids)
        self.client.get(url='/int/pages/{page_id}'.format(page_id=page_id))


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
