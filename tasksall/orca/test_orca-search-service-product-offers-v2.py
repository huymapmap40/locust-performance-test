# coding=utf-8
from locust import HttpUser, TaskSet, task, between
import random

from os.path import join, dirname
from functools import partial

def read_fixture_file(handler, filename):
    file_path = join(dirname(__file__), filename)
    with open(file_path) as f:
        data = handler(f)
    return data


load_fixtures = partial(read_fixture_file, lambda x: [i.strip() for i in x])


HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": "true",
    "X-Shopback-Country": "TW",
    "x-Shopback-domain": "www.shopback.com.tw"
}

OFFER_IDS = load_fixtures('orca_offer_ids.csv')
PRODUCT_URLS = load_fixtures('product_urls.csv')
PRODUCT_TITLES = load_fixtures('product_titles.csv')
SORTS = ['lp', 'hp', 'hb']

def get_product_offer_url():
    sort = random.choice(SORTS)
    url = "/search/v2/product/offer?includePriceHistory=true&sizePerPage=30&sort={}".format(sort)

    # 95% probability
    if random.randint(1, 100) > 5:
        offer_id = random.choice(OFFER_IDS)
        url = url + "&candidateOfferIds[]={}".format(offer_id)
    else:
        product_url = random.choice(PRODUCT_URLS)
        url = url + "&url={}".format(product_url)

    if random.randint(1, 100) > 5:
        product_title = random.choice(PRODUCT_TITLES)
        url = url + "&title={}".format(product_title)

    print(url)
    return url


class UserBehavior(TaskSet):
    @task(1)
    def get_product_offer(self):
        url = get_product_offer_url()
        with self.client.get(url, headers=HEADERS, name="/search/v2/product/offer", catch_response=True) as response:
          if response.status_code == 200:
            print(response.json()['offersResultType'])
            response.success()
        self.client.close()


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
