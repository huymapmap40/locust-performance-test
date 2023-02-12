from locust import TaskSet
import common
import random

keywords = common.readCSV("/locust-tasks/fixtures_product_autocomplete_%s.csv" % (common.COUNTRY.lower()))
brand_ids = common.readCSV("/locust-tasks/fixtures_product_brand_%s.csv" % (common.COUNTRY.lower()))
category_ids = common.readCSV("/locust-tasks/fixtures_product_category_%s.csv" % (common.COUNTRY.lower()))

class ProductSearchScenario(TaskSet):
    def __init__(self, parent):
        super(ProductSearchScenario, self).__init__(parent)

    def task(self):
        name = "/orca/search/product"
        url = self._generate_search_url()
        self.client.get(url, headers=common.HEADERS, name=name)
        
    def _generate_search_url(self):
        page_types = ["product", "category", "brand"]
        page_type = random.choice(page_types)

        sorts = ["lp", "hp", "hb"]
        sort = random.choice(sorts)
        
        page = 1
        size_per_page = 20
        include_non_affiliate_store = True
        
        url = "/search/product?page={}&sizePerPage={}&pageType={}&sort={}&includeNonAffiliateStore={}".format(
            page, size_per_page, page_type, sort, include_non_affiliate_store
        )

        if page_type == "product":
            keyword = random.choice(keywords)
            url = url + "&name={}".format(keyword[0])
        elif page_type == "category":
            category_id = random.choice(category_ids)
            url = url + "&categoryIds[]={}".format(category_id[0])
        elif page_type == "brand":
            brand_id = random.choice(brand_ids)
            url = url + "&brandIds[]={}".format(brand_id[0])
        print(url)
        return url