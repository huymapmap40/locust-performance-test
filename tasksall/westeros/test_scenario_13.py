from locust import task, tag, TaskSet
import common


class Scenario13(TaskSet):
    def __init__(self, parent):
        super(Scenario13, self).__init__(parent)
        self.search_keyword = 'iphone'
        self.cookies = common.COOKIES

    @tag('scenario13')
    @task
    def task13(self):
        self.client.get(url=f'{common.BASE_URL}/',
                        cookies=self.cookies,
                        headers=common.HEADERS, name='Scenario13 - /')
        self.client.get(url=f'{common.BASE_URL}/wes-api/orca/search/keyword?value={self.search_keyword}',
                        cookies=self.cookies,
                        headers=common.HEADERS,
                        name=f'Scenario13 - /wes-api/orca/search/keyword?value={self.search_keyword}')
