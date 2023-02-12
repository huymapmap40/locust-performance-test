# coding=utf-8
from locust import HttpLocust, TaskSet, task
import base64
import json
import random
import requests
import csv, random

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

def readCSV(fileName):
    with open(fileName, 'r') as f:
        r = csv.reader(f, delimiter=',')
        # next(r)  # skip header line
        return list(r)

# TW
product_keywords = readCSV("/locust-tasks/orca-autocomplete-tw.csv")
store_keywords = readCSV("/locust-tasks/orca-merchant-tw.csv")
category_ids = [10, 542, 67, 5, 8, 29, 6, 7, 54, 34, 4, 33, 1, 32, 11, 50, 63, 30, 14, 207, 59, 58, 55, 235, 27, 208, 51, 9, 2, 53, 248, 18, 66, 45, 25, 28, 476, 430, 472, 12, 390, 87, 249, 245, 42, 433, 38, 355, 61, 210]
brand_ids = [62, 111, 58, 1, 61, 37, 43, 31, 81, 119, 36, 72, 34, 159, 97, 44, 45, 25, 19, 98, 56, 120, 106, 21, 66, 14, 52, 3, 15, 23, 4, 198, 85, 59, 47, 29, 125, 39, 41, 9, 75, 82, 48, 22, 26, 104, 17, 10, 160, 54, 24]

# AU
# product_keywords = readCSV("/locust-tasks/orca-autocomplete-au.csv")
# store_keywords = readCSV("/locust-tasks/orca-merchant-au.csv")
# category_ids = [3013, 528, 534, 361, 3018, 213, 433, 204, 249, 518, 364, 232, 458, 220, 5009, 3012, 217, 3014, 250, 207, 206, 472, 280, 500, 91, 355, 475, 385, 541, 397, 380, 359, 211, 3010, 307, 499, 501, 360, 251, 242, 286, 209, 387, 358, 94, 235, 216, 96, 429, 3009, 460, 219, 238, 244, 112, 260, 370, 5011, 402, 87, 350, 540, 532, 259, 5007, 490, 453, 403, 270, 351, 404, 373, 111, 5003, 194, 5001, 477, 5008, 198, 168, 254, 388, 167, 236, 267, 222, 241, 279, 441, 434, 145, 288, 5004, 293, 176, 274, 109, 537, 285, 243, 5006, 300, 3000, 295, 296, 354, 247, 5010, 413, 502, 290, 82, 495, 374, 445, 498, 289, 395, 292, 308, 488, 491, 3001, 5002, 462, 85, 106, 496, 255, 248, 442, 108, 321, 538, 365, 256, 3007, 169, 186, 125, 317, 93, 362, 128, 182, 299, 140, 352, 225, 189, 3005, 298, 163, 454, 143, 3004, 152, 149, 466, 319, 89, 240, 3006, 519, 425, 366, 3011, 258, 90, 158, 237, 278, 261, 530, 443, 394, 5012, 430, 239, 363, 262, 377, 264, 516, 432, 348, 287, 151, 3008, 166, 284, 327, 273, 84, 372, 523, 3016, 191, 86, 179, 411, 371, 155, 141, 463, 122, 465, 148, 449, 5016, 436, 3002, 5019, 5005, 156, 116, 535, 200, 382, 448, 210, 100, 356, 245, 367, 3003, 282, 115, 427, 482, 396, 337, 381, 392, 252, 517, 478, 306, 418, 440, 531, 335, 154, 389, 336, 417, 3017, 5017, 276, 185, 450, 5015, 391, 121, 5014, 483, 188, 346, 291, 173, 357, 393, 136, 187, 405, 221, 120, 175, 423, 184, 386, 480];
# brand_ids = [2081, 136, 54, 649, 47, 2243, 1347, 781, 465, 2101, 50, 1830, 415, 1606, 233, 296, 85, 239, 70, 270, 432, 547, 454, 1481, 1815, 2223, 190, 140, 1051, 3, 200, 41, 882, 157, 1249, 84, 507, 816, 678, 776, 56, 4, 1164, 540, 1577, 81, 52, 249, 127, 2089, 2244, 1576, 1479, 225, 395, 1228, 1759, 385, 1216, 240, 1256, 841, 99, 2059, 1778, 869, 1630, 35, 232, 1603, 92, 227, 18, 17, 425, 1507, 87, 194, 187, 115, 179, 177, 1156, 142, 33, 1898, 43, 1844, 2235, 1533, 122, 954, 2225, 2229, 271, 1465, 274, 1459, 662, 545, 1505, 654, 262, 486, 116, 2237, 1511, 1473, 332, 1790, 28, 1554, 489, 359, 255, 520, 741, 1512, 1488, 802, 945, 1082, 315, 1814, 1609, 469, 1138, 550, 1873, 1263, 14, 1404, 49, 806, 1276, 1780, 78, 132, 1255, 482, 683, 10, 121, 1833, 188, 2178, 638, 671, 243, 2234, 380, 1608, 31, 397, 1444, 527, 244, 86, 45, 1596, 452, 1531, 1359, 88, 178, 1308, 1563, 67, 1579, 153, 137, 576, 267, 938, 106, 268, 496, 1030, 2019, 1141, 1643, 1548, 1613, 114, 1477, 1470, 812, 564, 702, 234, 764, 185, 361, 46, 1782, 1758, 1724, 428, 309, 2274, 574, 1420, 201, 2074, 1114, 60, 544, 356, 1101, 110, 888, 275, 750, 2149, 2236, 424, 2224, 1159, 13, 1472, 1464, 710, 698, 152, 1289, 592, 1580, 300, 1150, 2025, 1427, 1595, 1616, 619, 2228, 1234, 632, 1502, 1604, 1611, 2250, 184, 895, 2123, 321, 281, 1701, 79, 1178, 2152, 322, 1423, 1112, 1917, 883, 2232, 1806, 1175, 791, 156, 704, 2256, 1559, 1566, 29, 2214, 792, 6, 1104, 1684, 1267, 1367, 374, 1610, 96, 1225, 1338, 2273, 616, 650, 793, 863, 946, 637, 826, 1681, 266, 438, 302, 1621, 782, 593, 1636, 256, 90, 414, 1365, 1137]

sorts = ['lp', 'hp', 'hb']


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
    sort = random.choice(sorts)
    url = "/search/product?page={}&sizePerPage={}&pageType={}&sort={}&includeNonAffiliateStore={}".format(
        page, size_per_page, page_type, sort, include_non_affiliate_store
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

    @task(3)
    def search_product_product(self):
        keyword = random.choice(product_keywords)
        url = get_search_url('product', keyword)
        self.client.get(url, headers=HEADERS, name="/orca/search/product - product - product keyword")
        self.client.close()

    @task(5)
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


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
