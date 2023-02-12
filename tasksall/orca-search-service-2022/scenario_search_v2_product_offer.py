from unicodedata import name
from locust import task, tag, TaskSet
import common
import random

class SearchV2ProductOfferScenario(TaskSet):
    OFFER_IDS = common.load_fixtures('/locust-tasks/fixtures_product_offer_ids_{}.csv'.format(common.COUNTRY.lower()))
    PRODUCT_URLS = common.load_fixtures('/locust-tasks/fixtures_product_urls_{}.csv'.format(common.COUNTRY.lower()))
    PRODUCT_TITLES = common.load_fixtures('/locust-tasks/fixtures_product_titles_{}.csv'.format(common.COUNTRY.lower()))
    SORTS = ['lp', 'hp', 'hb']
  
    @tag('search_v2_product_offer')
    @task
    def task(self):
        name = "/search/v2/product/offer"
        url = self._get_product_offer_url()
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        
    def _get_product_offer_url(self):
        sort = random.choice(self.SORTS)
        url = "/search/v2/product/offer?includePriceHistory=true&sizePerPage=30&sort={}".format(sort)

        # 95% probability
        if random.randint(1, 100) > 5:
            offer_id = random.choice(self.OFFER_IDS)
            url = url + "&candidateOfferIds[]={}".format(offer_id)
        else:
            product_url = random.choice(self.PRODUCT_URLS)
            url = url + "&url={}".format(product_url)

        if random.randint(1, 100) > 5:
            product_title = random.choice(self.PRODUCT_TITLES)
            url = url + "&title={}".format(product_title)

        print(url)
        return url