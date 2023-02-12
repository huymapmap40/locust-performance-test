from locust import task, tag, TaskSet
import common


class Scenario17(TaskSet):
    def __init__(self, parent):
        super(Scenario17, self).__init__(parent)
        self.cookies = common.COOKIES

    @tag('scenario17')
    @task
    def task17(self):
        self.client.get(url=f'{common.BASE_URL}/cashback',
                        cookies=self.cookies,
                        headers=common.HEADERS,
                        name='Scenario17 - /cashback')
        self.client.get(url=f'{common.BASE_URL}/click-activity',
                        headers=common.HEADERS,
                        cookies=self.cookies,
                        name='Scenario17 - /click-activity')
