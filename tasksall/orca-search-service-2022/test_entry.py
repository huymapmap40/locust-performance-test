# Testing Steps Locally
# 1. change the COUNTRY and DOMAIN variable in scenarios/common.py
# 2. port-forward the orca-search-service from COUNTRY
# 3. run locust in root of the repo: ./scripts/local_start.sh host.docker.internal:8080 test_entry tasks/orca-search-service-2022

# Testing Steps On K8S
# [Workaround] 0. To fix the `entity too large: limit is 314572` issue, please remove all unused file in tasks folder in this testing. That's including the unused script and fixtures.
# 1. change the COUNTRY and DOMAIN variable in scenarios/common.py
# 2. change the COUNTRY target host in environments/test_orca-search-service-2022.yaml
# 3. Deploy: ./install.sh environments/test_orca-search-service-2022.yaml locust-orca-search-service-{CC} sb-dep-dev-team-orca
# 4. Testing: ./forward.sh sb-dep-dev-team-orca
# 5. Destroy: ./remove.sh sb-dep-dev-team-orca

from locust import HttpUser, task, between
import common
from scenario_mobile_powerscreen import MobilePowerscreenScenario
from scenario_price_drop import PriceDropScenario
from scenario_product_autocomplete import ProductAutocompleteScenario
from scenario_product_detail import ProductDetailScenario
from scenario_search_voucher import SearchVoucherScenario
from scenario_recommend_product import RecommendProductScenario
from scenario_search_keyword_voucher import SearchVoucherKeywordScenario
from scenario_search_product_offer import SearchProductOfferScenario
from scenario_search_v2_product_offer import SearchV2ProductOfferScenario
from scenario_search_keyword_trend import SearchKeywordTrendScenario
from scenario_search_keyword_trend_v2 import SearchKeywordTrendV2Scenario
from scenario_search_content_order import SearchContentOrderScenario
from scenario_search_merchant_mapping import SearchMerchantMappingScenario
from scenario_product_ams_merchant import ProductAMSMerchantScenario
from scenario_product_search import ProductSearchScenario
from scenario_store_autocomplete import StoreAutocompleteScenario
from scenario_store_search import StoreSearchScenario

TASK_DISTRIBUTION_BY_COUNTRY = {
    "AU": {
        "merchant_mapping": 0,
        "mobile_powerscreen": 0,
        "price_drop": 24,
        "product_detail": 9,
        "recommend_product": 2,
        "search_ams_merchant_product": 0,
        "search_content_order": 0,
        "search_product": 9,
        "search_product_keyword":18,
        "search_product_offer": 0,
        "search_product_offer_v2": 0,
        "search_store": 3,
        "search_store_keyword": 16,
        "search_voucher": 1,
        "search_voucher_keyword":  17,
        "search_trending_keyword": 0,
        "search_trending_keyword_v2": 3,
    },
    "TW": {
        "merchant_mapping": 0,
        "mobile_powerscreen": 0,
        "price_drop": 21,
        "product_detail": 8,
        "recommend_product": 3,
        "search_ams_merchant_product": 0,
        "search_content_order": 0,
        "search_product": 9,
        "search_product_keyword": 5,
        "search_product_offer": 26,
        "search_product_offer_v2": 16,
        "search_store": 2,
        "search_store_keyword": 5,
        "search_voucher": 0,
        "search_voucher_keyword": 0,
        "search_trending_keyword": 0,
        "search_trending_keyword_v2": 4,
    },
    "ID": {
        "merchant_mapping": 3,
        "mobile_powerscreen": 4,
        "price_drop": 0,
        "product_detail": 32,
        "recommend_product": 0,
        "search_ams_merchant_product": 9,
        "search_content_order": 0,
        "search_product": 24,
        "search_product_keyword": 10,
        "search_product_offer": 0,
        "search_product_offer_v2": 0,
        "search_store": 6,
        "search_store_keyword": 8,
        "search_voucher": 0,
        "search_voucher_keyword": 0,
        "search_trending_keyword": 2,
        "search_trending_keyword_v2": 2,
    },
}

TASK_DISTRIBUTION = TASK_DISTRIBUTION_BY_COUNTRY[common.COUNTRY]

class SimulatedUserAction(HttpUser):
    wait_time = between(1, 3)

    @task(TASK_DISTRIBUTION['merchant_mapping'])
    def merchant_mapping(self):
        SearchMerchantMappingScenario(self).task()

    @task(TASK_DISTRIBUTION['mobile_powerscreen'])
    def mobile_powerscreen(self):
        MobilePowerscreenScenario(self).task()

    @task(TASK_DISTRIBUTION['price_drop'])
    def price_drop(self):
        PriceDropScenario(self).task()

    @task(TASK_DISTRIBUTION['product_detail'])
    def product_detail(self):
        ProductDetailScenario(self).task()

    @task(TASK_DISTRIBUTION['recommend_product'])
    def recommend_product(self):
        RecommendProductScenario(self).task()

    @task(TASK_DISTRIBUTION['search_ams_merchant_product'])
    def search_ams_merchant_product(self):
        ProductAMSMerchantScenario(self).task()

    @task(TASK_DISTRIBUTION['search_content_order'])
    def search_content_order(self):
        SearchContentOrderScenario(self).task()

    @task(TASK_DISTRIBUTION['search_product'])
    def search_product(self):
        ProductSearchScenario(self).task()

    @task(TASK_DISTRIBUTION['search_product_keyword'])
    def search_product_keyword(self):
        ProductAutocompleteScenario(self).task()

    @task(TASK_DISTRIBUTION['search_product_offer'])
    def search_product_offer(self):
        SearchV2ProductOfferScenario(self).task()

    @task(TASK_DISTRIBUTION['search_product_offer_v2'])
    def search_product_offer_v2(self):
        SearchProductOfferScenario(self).task()

    @task(TASK_DISTRIBUTION['search_store'])
    def search_store(self):
        StoreSearchScenario(self).task()

    @task(TASK_DISTRIBUTION['search_store_keyword'])
    def search_store_keyword(self):
        StoreAutocompleteScenario(self).task()

    @task(TASK_DISTRIBUTION['search_voucher'])
    def search_voucher(self):
        SearchVoucherScenario(self).task()

    @task(TASK_DISTRIBUTION['search_voucher_keyword'])
    def search_voucher_keyword(self):
        SearchVoucherKeywordScenario(self).task()

    @task(TASK_DISTRIBUTION['search_trending_keyword'])
    def search_trending_keyword(self):
        SearchKeywordTrendScenario(self).task()

    @task(TASK_DISTRIBUTION['search_trending_keyword_v2'])
    def search_trending_keyword_v2(self):
        SearchKeywordTrendV2Scenario(self).task()
