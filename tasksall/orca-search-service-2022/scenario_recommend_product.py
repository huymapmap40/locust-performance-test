from unicodedata import name
from locust import task, tag, TaskSet
import common
import random

class RecommendProductScenario(TaskSet):
    KEYWORDS = common.load_fixtures('/locust-tasks/fixtures_product_titles_{}.csv'.format(common.COUNTRY.lower()))
  
    @tag('recommend_product_by_search_history')
    @task(1)
    def task(self):
        name = "/recommendation/product/by-search-history"
        url = self._get_product_offer_url()
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        
    def _get_product_offer_url(self):
        url = "/recommendation/product/by-search-history?"

        keyword = random.choice(self.KEYWORDS)
        url = url + "keywords[]={}".format(keyword)

        print(url)
        return url