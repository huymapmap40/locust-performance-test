from locust import task, tag, TaskSet
import westeros_common


class Scenario4(TaskSet):
    def __init__(self, parent):
        super(Scenario4, self).__init__(parent)
        # need to create a campaign page with this slug before executing the test
        self.campaign = westeros_common.CAMPAIGN
        self.cookies = westeros_common.COOKIES

    @tag('scenario4')
    @task
    def task3(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/',
                        cookies=self.cookies,
                        name='Scenario4 - /')
        self.client.get(url=f'{westeros_common.BASE_URL}/{self.campaign}',
                        cookies=self.cookies,
                        name=f'Scenario4 - /{self.campaign}')
