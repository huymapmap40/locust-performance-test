from locust import task, tag, TaskSet
import westeros_common


class Scenario2(TaskSet):
    def __init__(self, parent):
        super(Scenario2, self).__init__(parent)
        self.cookies = westeros_common.COOKIES

    @tag('scenario2')
    @task
    def task2(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/',
                        cookies=self.cookies, name='Scenario2 - /')
        self.client.get(url=f'{westeros_common.BASE_URL}/all-stores',
                        cookies=self.cookies,
                        name='Scenario2 - /all-stores')
