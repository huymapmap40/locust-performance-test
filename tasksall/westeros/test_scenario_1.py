from locust import task, tag, TaskSet
import common


class Scenario1(TaskSet):
    def __init__(self, parent):
        super(Scenario1, self).__init__(parent)
        self.cookies = common.COOKIES

    @tag('scenario1')
    @task
    def task1(self):
        self.client.get(
            url=f'{common.BASE_URL}/',
            cookies=self.cookies,
            name='Scenario1 - /'
        )

