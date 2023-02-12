import common
from locust import TaskSet

class SearchKeywordTrendV2Scenario(TaskSet):
    def task(self):
        name = '/search/v2/keyword/trend'
        url = '/search/v2/keyword/trend'
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        