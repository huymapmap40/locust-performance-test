import common
from locust import TaskSet

class SearchMerchantMappingScenario(TaskSet):
    def task(self):
        name = '/merchant/mapping'
        url = '/merchant/mapping'
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        