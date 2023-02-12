from locust import task, tag, TaskSet
import westeros_common


class Scenario17(TaskSet):
    def __init__(self, parent):
        super(Scenario17, self).__init__(parent)
        self.cookies = westeros_common.COOKIES

    @tag('scenario17')
    @task
    def task17(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/api/cashback-overview/shopping-trips',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name='Scenario17 - /api/cashback-overview/shopping-trips')
        self.client.get(url=f'{westeros_common.BASE_URL}/click-activity',
                        headers=westeros_common.HEADERS,
                        cookies=self.cookies,
                        name='Scenario17 - /click-activity')
