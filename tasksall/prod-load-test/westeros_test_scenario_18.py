from locust import HttpUser, TaskSet, task, between, tag
import westeros_common


class Scenario18(TaskSet):
    def __init__(self, parent):
        super(Scenario18, self).__init__(parent)
        self.cookies = westeros_common.COOKIES

    @tag('scenario18')
    @task
    def task1(self):
        self.client.get(
            url=f'{westeros_common.BASE_URL}/?cache=no-cache',
            cookies=self.cookies,
            name='Scenario18 - no cache'
        )


class WebsiteUser(HttpUser):
    tasks = [Scenario18]
    wait_time = between(10, 50)
