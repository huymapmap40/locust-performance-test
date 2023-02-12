from locust import task, tag, TaskSet
import westeros_common


class Scenario15(TaskSet):
    def __init__(self, parent):
        super(Scenario15, self).__init__(parent)
        self.category_name = 'Smartphone'
        self.category_id = 82
        self.cookies = westeros_common.COOKIES

    @tag('scenario15')
    @task
    def task15(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name='Scenario15 - /')
        self.client.get(url=f'{westeros_common.BASE_URL}/product/category/{self.category_name}/{self.category_id}',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS, name=f'Scenario15 - /product/category/{self.category_name}/{self.category_id}')
