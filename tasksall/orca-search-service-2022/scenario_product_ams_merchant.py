from locust import TaskSet
import common
import random

# only for ID
merchant_ids = common.readCSV("/locust-tasks/fixtures_product_merchant_%s.csv" % (common.COUNTRY.lower()))
class ProductAMSMerchantScenario(TaskSet):
    def task(self):
        name = '/search/ams/merchant/product'
        merchant_id = random.choice(merchant_ids)
        url = '/search/ams/merchant/product?productType=trending&merchantIds[]=%s' %(merchant_id[0])
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)