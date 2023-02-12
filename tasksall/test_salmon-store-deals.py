from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.web_headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210',
            'X-Shopback-Domain': 'www.shopback.com.tw',
        }
        self.storeIds = [1071,2135,2136,2138,2146,2150,2156,2157,2158,2160,2162,2163,2166,2167,2205,2240,2295,40,43,46,49,157,165,992,363,388,432,534,595,718,901,927,943,988,1031,1078,1561,1799,1723,1783,1787,1794,1796,1798,1803,1804,1826,1837,1840,1885,1886,1888,1889,1890,1891,1941,1942,1945,2009,2011,2016,2017,2030,2032,2033,2034,2035,2039,2040,2042,2043,2052,2074,2055,2056,2057,2059,2061,2064,2081,2091,2092,2094,2097,2110,102,22236,271,22242,318,22246,671,22252,838,22259,1012,22265,1790,22273,1793,22280,1887,22282,1999,22284,2024,22297,2038,22305,2227,22313,81,2336,1789,2159]
        self.storeId = random.choice(self.storeIds)
        
    @task
    def getIntStoreDeals(self):
        self.client.get(
            url='/int/stores/' + str(self.storeId) + '/deals',
            headers=self.web_headers,
        )
   


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(10, 50)
