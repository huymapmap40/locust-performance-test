from unicodedata import name
from locust import task, tag, TaskSet
import common
import random

class SearchVoucherKeywordScenario(TaskSet):
    KEYWORDS = common.load_fixtures('/locust-tasks/fixtures_voucher_keywords_{}.csv'.format(common.COUNTRY.lower()))
  
    @tag('search_voucher_keywords')
    @task(1)
    def task(self):
        name = "/search/keyword/voucher"
        url = self._get_product_offer_url()
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        
    def _get_product_offer_url(self):
        url = "/search/keyword/voucher?"

        keyword = random.choice(self.KEYWORDS)
        url = url + "value={}".format(keyword)

        print(url)
        return url