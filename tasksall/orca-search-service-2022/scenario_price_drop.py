import common
from locust import TaskSet

class PriceDropScenario(TaskSet):
    def task(self):
        name = '/uhs/product/price-drop'
        url = '/uhs/product/price-drop'
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
