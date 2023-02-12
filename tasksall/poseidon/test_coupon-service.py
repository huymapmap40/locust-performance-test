from locust import HttpUser, TaskSet, task, between
from random import choice, choices, randrange

DEFAULT_HEADERS = {
    'Content-Type': 'application/json'
}
MERCHANT_IDS = ['19298', '19311', '19355', '18133', '18133', '18728']
COUPON_IDS = ['1', '2', '3', '4', '5', '6']
SLOW_RESPONSE_THRESHOLD_SECS = 2


class GetMerchantStats(TaskSet):
    def coupon_merchant_stats(self, ver='v1', params=None, suffix_name='by merchant ids'):
        url = f'/{ver}/coupons/merchant-stats'

        self.client.get(
            url=url,
            headers=DEFAULT_HEADERS,
            params=params,
            name=f'Get coupon merchant stats {ver} {suffix_name}'
        )

    @task
    def coupon_merchant_stats_v1(self):
        merchant_ids = ','.join(choices(MERCHANT_IDS, k=randrange(0, 6)))
        self.coupon_merchant_stats('v1', {'merchantIds': merchant_ids})

    @task
    def coupon_merchant_stats_v2(self):
        merchant_ids = ','.join(choices(MERCHANT_IDS, k=randrange(0, 6)))
        self.coupon_merchant_stats('v2', {'merchantIds': merchant_ids})

    @task
    def coupon_merchant_stats_v2_all(self):
        suffix_name = 'by all is true'
        self.coupon_merchant_stats('v2', {'all': 'true'}, suffix_name)

    wait_time = between(0.5, 10)


class InternalGetCoupons(TaskSet):
    url = '/v1/internal/coupons'

    @task
    def internal_get_coupons_by_merchant_ids(self):
        name = 'Get coupons by merchant ids'
        merchant_ids = ','.join(choices(MERCHANT_IDS, k=randrange(0, 6)))
        params = {
            'merchantIds': merchant_ids
        }

        self.client.get(
            url=self.url,
            headers=DEFAULT_HEADERS,
            params=params,
            name=name
        )

    @task
    def internal_get_coupons_by_coupon_code_ids(self):
        name = 'Get coupons by coupon code ids'
        coupon_ids = ','.join(choices(COUPON_IDS, k=randrange(1, 6)))
        params = {
            'couponCodeIds': coupon_ids
        }

        self.client.get(
            url=self.url,
            headers=DEFAULT_HEADERS,
            params=params,
            name=name
        )

    wait_time = between(0.5, 10)


class GetTopMerchants(TaskSet):
    platforms = ('web', 'ios', 'android')
    top_merchants_api_url = '/v1/coupons/top-merchants'
    trending_merchants_api_url = '/v1/coupons/trending-merchants'

    @task
    def get_top_coupon_merchants(self):
        with self.client.get(
            url=f'{self.top_merchants_api_url}?platform={choice(self.platforms)}',
            name=self.top_merchants_api_url,
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
    def get_trending_coupon_merchants(self):
        with self.client.get(
                url=f'{self.trending_merchants_api_url}?platform={choice(self.platforms)}',
                name=self.trending_merchants_api_url,
                headers=DEFAULT_HEADERS,
                catch_response=True
        ) as response:
            if not response.ok:
                response.failure('Got bad response!')
            elif response.elapsed.total_seconds() > SLOW_RESPONSE_THRESHOLD_SECS:
                response.failure('Response takes too long!')
            else:
                response.success()


class WebsiteUser(HttpUser):
    tasks = [
        GetMerchantStats,
        InternalGetCoupons,
        GetTopMerchants
    ]

    min_wait = 0
    max_wait = 0
