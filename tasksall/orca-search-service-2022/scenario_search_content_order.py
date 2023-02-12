from locust import TaskSet
import common
import random

keywords = common.load_fixtures('/locust-tasks/fixtures_content_order_keywords_{}.csv'.format(common.COUNTRY.lower()))

class SearchContentOrderScenario(TaskSet):
    def task(self):
        keyword = random.choice(keywords)
        name = '/search/content/order'
        url = '/search/content/order?value={}'.format(keyword)
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        