from locust import task, tag, TaskSet
import westeros_common
import random

class Scenario14(TaskSet):
    def __init__(self, parent):
        super(Scenario14, self).__init__(parent)
        self.merchants = random.choice(westeros_common.MERCHANT)
        self.search_keyword = self.merchants['MERCHANT_SHORTNAME']
        self.cookies = westeros_common.COOKIES

    @tag('scenario14')
    @task
    def task14(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name='Scenario14 - /')
        self.client.get(url=f'{westeros_common.BASE_URL}/wes-api/orca/search/keyword?value={self.search_keyword}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name=f'Scenario14 - /wes-api/orca/search/keyword?value={self.search_keyword}')
