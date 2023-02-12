import common
from locust import TaskSet

class SearchKeywordTrendScenario(TaskSet):
    def task(self):
        name = '/search/keyword/trend'
        url = '/search/keyword/trend'
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        