import json
import random
import os

from locust import HttpUser, TaskSet, task

from utils import load_fixtures

SHOPBACK_USER_TOKEN = os.getenv('SHOPBACK_USER_TOKEN')
SHOPBACK_API_KEY_SECRET_CONSUMER = os.getenv('SHOPBACK_API_KEY_SECRET_CONSUMER')
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Agent': 'sbconsumeragent/1.0',
    'X-Shopback-Internal': SHOPBACK_API_KEY_SECRET_CONSUMER,
    'Authorization': f'JWT {SHOPBACK_USER_TOKEN}',
}
ACCOUNT_HEADERS = {
    **DEFAULT_HEADERS,
    'X-Shopback-Access-Token': '<Need to get from sbet cookie>',
    'X-Shopback-Refresh-Token': '<Need to get from refersh cookie>',
    'X-Shopback-Client-User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
}
# Merchant ids on Staging SG
MERCHANT_IDS = [18145, 18645, 19335, 19307, 19329]
SLOW_RESPONSE_THRESHOLD_SECS = 2
PRODUCT_URLS = load_fixtures('product_urls.txt')
PRODUCT_ID_FOR_FAVORITE_VERIFICATION = '24hpchome:DYAJGA-1900AY96S-000'


class UserBehavior(TaskSet):
    favorites = '/whale/products/favorites'
    favorites_verification = '/whale/products/favorites/verification'

    @task
    def get_favorites(self):
        if not SHOPBACK_USER_TOKEN:
            raise Exception('Token CANNOT be empty')

        with self.client.get(
            url=f'{self.favorites}',
            name=self.favorites,
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

    @task
    def get_favorites_verification(self):
        if not SHOPBACK_USER_TOKEN:
            raise Exception('Token CANNOT be empty')

        with self.client.get(
            url=f'{self.favorites_verification}?productIds[]={PRODUCT_ID_FOR_FAVORITE_VERIFICATION}',
            name=self.favorites_verification,
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

    @task
    def post_favorites_verification(self):
        if not SHOPBACK_USER_TOKEN:
            raise Exception('Token CANNOT be empty')

        with self.client.post(
            url=f'{self.favorites_verification}',
            data=json.dumps({
                'productIds': [PRODUCT_ID_FOR_FAVORITE_VERIFICATION],
            }),
            name=f'POST: {self.favorites_verification}',
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                print(response)
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class ProductOffersTaskSet(TaskSet):
    product_offers = '/whale/products/offers'
    product_v2_offers = '/whale/products/v2/offers'

    @task
    def get_product_offers(self):
        with self.client.get(
            url=f'{self.product_offers}?url={random.choice(PRODUCT_URLS)}',
            name=self.product_offers,
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

    @task
    def post_product_v2_offers(self):
        with self.client.post(
            url=f'{self.product_v2_offers}',
            data=json.dumps({
                'url': random.choice(PRODUCT_URLS),
            }),
            name=self.product_v2_offers,
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class PriceHistoryTaskSet(TaskSet):
    price_history = '/whale/products/price-history'

    @task
    def get_price_history(self):
        with self.client.get(
            url=f'{self.price_history}?url=http://www.rakuten.com.tw?run=io.write',
            name=self.price_history,
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class Accounts(TaskSet):
    accounts_path = '/whale/accounts'

    @task
    def get_accounts(self):
        with self.client.get(
            url=self.accounts_path,
            name=self.accounts_path,
            headers=ACCOUNT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

    @task
    def get_accounts_cashbacks_latest(self):
        with self.client.get(
            url=f'{self.accounts_path}/cashbacks/latest',
            name=f'{self.accounts_path}/cashbacks/latest',
            headers=ACCOUNT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class Merchants(TaskSet):
    merchants_path = '/whale/merchants'

    @task
    def get_terms_conditions(self):
        with self.client.get(
            url=f'/whale/merchants/terms-and-conditions/{random.choice(MERCHANT_IDS)}',
            name='terms-and-conditions',
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(
                    f'Got bad response, statue: {response.status_code} {response.content}'
                )
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()
    
    @task
    def get_merchants(self):
        with self.client.get(
            url=f'{self.merchants_path}',
            name=f'{self.merchants_path}',
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(
                    f'Got bad response, statue: {response.status_code} {response.content}'
                )
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success() 


class Recommendation(TaskSet):
    recommendation_path = '/whale/recommendation'

    @task
    def get_personalized_merchants(self):
        with self.client.get(
            url=f'{self.recommendation_path}/merchants/personalized',
            name=f'{self.recommendation_path}/merchants/personalized',
            headers=DEFAULT_HEADERS,
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(
                    f'Got bad response, statue: {response.status_code} {response.content}'
                )
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

class Settings(TaskSet):
    settings_path = '/whale/settings'

    @task
    def get_extension_settings(self):
        with self.client.get(
            url=f'{self.settings_path}',
            name=f'{self.settings_path}',
            headers={
                'x-shopback-extension-version': '6.6.0'
            },
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(
                    f'Got bad response, statue: {response.status_code} {response.content}'
                )
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()

class Coupons(TaskSet):
    coupons_path = '/whale/coupons'

    @task
    def get_merchant_coupons(self):
        with self.client.get(
            url=f'{self.coupons_path}/merchant/{random.choice(MERCHANT_IDS)}',
            name=f'{self.coupons_path}/merchant/{random.choice(MERCHANT_IDS)}',
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(
                    f'Got bad response, statue: {response.status_code} {response.content}'
                )
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class WebsiteUser(HttpUser):
    tasks = [
        Accounts,
        Merchants,
        Recommendation,
        UserBehavior,
        ProductOffersTaskSet,
        PriceHistoryTaskSet,
        Settings,
        Coupons,
    ]
    min_wait = 1000
    max_wait = 1000
