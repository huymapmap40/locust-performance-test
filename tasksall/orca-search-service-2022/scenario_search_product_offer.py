from unicodedata import name
from locust import task, tag, TaskSet
import common
import random

class SearchProductOfferScenario(TaskSet):
    OFFER_IDS = common.load_fixtures('/locust-tasks/fixtures_product_offer_ids_{}.csv'.format(common.COUNTRY.lower()))
    PRODUCT_URLS = common.load_fixtures('/locust-tasks/fixtures_product_urls_{}.csv'.format(common.COUNTRY.lower()))
  
    @tag('search_product_offer')
    @task
    def task(self):
        name = "/search/product/offer"
        url = self._get_product_offer_url()
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
        
    def _get_product_offer_url(self):
      url = "/search/product/offer?includePriceHistory=true&sizePerPage=1"

      # 95% probability
      if random.randint(1, 100) > 5:
          offer_id = random.choice(self.OFFER_IDS)
          url = url + "&candidateOfferIds[]={}".format(offer_id)
      else:
          product_url = random.choice(self.PRODUCT_URLS)
          url = url + "&url={}".format(product_url)

      print(url)
      return url