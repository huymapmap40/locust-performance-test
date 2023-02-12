# coding=utf-8
from locust import HttpUser, TaskSet, task, between
from os.path import join, dirname
from functools import partial
import random
import base64
import json
import requests

SIMILAR_KEYWORD = False # boolean

USE_IRON_GATE = "true"  # string

USE_API_GATEWAY = False  # boolean
API_GATEWAY = "http://gateway-staging.shopback.com.tw"

# Login variable
EMAIL = "andy.li@shopback.com"  # 2464051
PASSWORD = "abcd1234"
COUNTRY = "TW"
DOMAIN = "www.shopback.com.tw"

# Without login
ACCOUNT_ID = 2461721  # andy.test@shopback.com

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": USE_IRON_GATE,
    "X-Shopback-Country": COUNTRY,
    "x-Shopback-domain": DOMAIN,
    "x-shopback-recaptcha-type": "bypass"
}

def read_fixture_file(handler, filename):
    file_path = join(dirname(__file__), filename)
    with open(file_path) as f:
        data = handler(f)
    return data

load_fixtures = partial(read_fixture_file, lambda x: [i.strip() for i in x])

# TW
product_keyword_file_name = "orca-product-keyword-cache-tw.csv" if SIMILAR_KEYWORD else "orca-autocomplete-tw.csv"
store_keyword_file_name = "orca-merchant-keyword-cache-tw.csv" if SIMILAR_KEYWORD else "orca-merchant-tw.csv"
product_keywords = load_fixtures(product_keyword_file_name)
store_keywords = load_fixtures(store_keyword_file_name)
category_ids = [10, 542, 67, 5, 8, 29, 6, 7, 54, 34]
brand_ids = [62, 111, 58, 1, 61, 37, 43, 31, 81, 119]

# AU
# product_keyword_file_name = "orca-product-keyword-cache-au.csv" if SIMILAR_KEYWORD else "orca-autocomplete-au.csv"
# store_keyword_file_name = "orca-merchant-keyword-cache-au.csv" if SIMILAR_KEYWORD else "orca-merchant-au.csv"
# product_keywords = load_fixtures(product_keyword_file_name)
# store_keywords = load_fixtures(store_keyword_file_name)
# category_ids = [3013, 528, 534, 361, 3018, 213, 433, 204, 249, 518];
# brand_ids = [2081, 136, 54, 649, 47, 2243, 1347, 781, 465, 2101]

def login(email, password):
    url = "{}/members/sign-in".format(API_GATEWAY)
    payload = json.dumps({
        "email": email,
        "password": password,
        "client_user_agent": "test"
    })
    response = requests.request("POST", url, headers=HEADERS, data=payload)
    if response.status_code == 200:
        if 'auth' in response.json():
            return response.json()['auth']['access_token']
    print('Cant to get token {}'.format(response.json()))
    exit(1)


def generate_jwt_token(account_id):
    authorization_content = json.dumps({
        "uuid": "479c94048a8e410694ea24fc17302906",
        "iss": DOMAIN,
        "issuedAt": 1577477107.184,
        "iat": 1577477107,
        "exp": 1578773107,
        "id": account_id
    })
    return base64.b64encode(authorization_content.encode('utf-8')).decode('utf-8')


def get_search_url(page_type, keyword=None):
    page = 1
    size_per_page = 20
    include_non_affiliate_store = True
    url = "/search/product?page={}&sizePerPage={}&pageType={}&includeNonAffiliateStore={}".format(
        page, size_per_page, page_type, include_non_affiliate_store
    )
    if USE_API_GATEWAY is True:
        url = '/orca' + url
    if page_type == 'product':
        url = url + "&name={}".format(keyword)
    elif page_type == 'category':
        category_id = random.choice(category_ids)
        url = url + "&categoryIds[]={}".format(category_id)
    elif page_type == 'brand':
        brand_id = random.choice(brand_ids)
        url = url + "&brandIds[]={}".format(brand_id)
    print(url)
    return url

def get_search_preview_url(keyword=None):
    page = 1
    size_per_page = 20
    page_type = "product"
    url = "/search/product/preview?page={}&sizePerPage={}&pageType={}&name={}".format(
        page, size_per_page, page_type, keyword
    )
    if USE_API_GATEWAY is True:
        url = '/orca' + url
    print(url)
    return url

class UserBehaviorPreview(TaskSet):
    if USE_API_GATEWAY is True:
        token = login(EMAIL, PASSWORD)
    else:
        token = generate_jwt_token(ACCOUNT_ID)
    print('Token: ', token)
    HEADERS['Authorization'] = 'JWT {}'.format(token)

    @task(1)
    def search_product_preview(self):
        keyword = random.choice(product_keywords)
        url = get_search_preview_url(keyword)
        self.client.get(url, headers=HEADERS, name="/orca/search/product/preview")
        self.client.close()


class UserBehavior(TaskSet):
    if USE_API_GATEWAY is True:
        token = login(EMAIL, PASSWORD)
    else:
        token = generate_jwt_token(ACCOUNT_ID)
    print('Token: ', token)
    HEADERS['Authorization'] = 'JWT {}'.format(token)

    # url = API_GATEWAY + get_search_url('product')
    # req = requests.request('GET', url, headers=HEADERS)
    # print(req.text)

    @task(1)
    def search_product_product(self):
        keyword = random.choice(product_keywords)
        url = get_search_url('product', keyword)
        self.client.get(url, headers=HEADERS, name="/orca/search/product - product - product keyword")
        self.client.close()

    @task(1)
    def search_product_store(self):
        keyword = random.choice(store_keywords)
        url = get_search_url('product', keyword)
        self.client.get(url, headers=HEADERS, name="/orca/search/product - product - store keyword")
        self.client.close()

    @task(1)
    def search_category(self):
        url = get_search_url('category')
        self.client.get(url, headers=HEADERS, name="/orca/search/product - category")
        self.client.close()

    @task(1)
    def search_brand(self):
        url = get_search_url('brand')
        self.client.get(url, headers=HEADERS, name="/orca/search/product - brand")
        self.client.close()


class WebsiteUser(HttpUser):
    tasks = [UserBehavior] 
    wait_time = between(1, 3)
