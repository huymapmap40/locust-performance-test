from locust import HttpUser, TaskSet, task, between
import random

headers = {
    'X-Shopback-Agent': 'sbconsumeragent/1.0',
    'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210',
}
mobile_content_service_base_url = 'http://mobile-content-service'


# mobile_content_service_base_url = 'http://mobile-content-service.internal.staging-sg.non-prod.svc.shopback.com'


def extract_banner_group_id(containers):
    for container in containers:
        for fragment in container['fragments']:
            if fragment['type'] == 'campaign:banner-group':
                return fragment['dataId']


class UserBehavior(TaskSet):
    merchant_ids = []
    banner_group_id = None

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def on_start(self):
        response = self.client.get(
            url='{mobile_content_service_base_url}/mobile-content/adm/v1/merchants'.format(
                mobile_content_service_base_url=mobile_content_service_base_url),
            headers=headers
        )
        merchants = response.json()['data']
        self.merchant_ids = [m['merchantId'] for m in merchants[0:10]]

        response = self.client.get(
            url='/v1/page-config?slug=auto-test&template=campaign',
        )
        containers = response.json()['containers']
        self.banner_group_id = extract_banner_group_id(containers)

    @task(30)
    def get_page_config(self):
        query = random.choice(
            ['slug=shopee', 'slug=lazada', 'slug=taobao', 'slug=newhomepage&template=home', 'slug=raf&template=raf'])
        self.client.get(
            url='/v1/page-config?' + query,
        )

    @task(20)
    def get_offer_ordering(self):
        merchant_id = random.choice(self.merchant_ids)
        self.client.get(
            url='/v1/offer-ordering/stores/{merchant_id}'.format(merchant_id=merchant_id),
        )

    @task(2)
    def get_banner_group(self):
        self.client.get(
            url='/v1/banner-group/{banner_group_id}'.format(banner_group_id=self.banner_group_id),
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
