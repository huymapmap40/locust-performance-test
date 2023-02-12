import csv
import random
from locust import HttpLocust, TaskSet


def readCSV(fileName):
    with open(fileName, 'r') as f:
        r = csv.reader(f, delimiter=',')
        # next(r)  # skip header line
        return list(r)


offerIds = readCSV("offerIds.csv")


def redirect_test(l):
    offerId = random.choice(offerIds)
    endpoint = '/product/redirect/v2/'+offerId[0]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "JWT eyJ1dWlkIjoiODI3YWE5ZDM4ZTRmNDYwOGFjNjA5ZDZjNDEzMzJkYzIiLCJpc3MiOiJ3d3cuc2hvcGJhY2suY29tLnR3IiwiaXNzdWVkQXQiOjE1OTU1NzU0ODAuNjQsImlhdCI6MTU5NTU3NTQ4MCwiZXhwIjoxNTk1NjYxODgwLCJpZCI6MjQ2NDA1MX0=",
        "X-Shopback-Country": "TW",
        "x-shopback-domain": "www.shopback.com.tw",
        "X-Shopback-Language": "zh",
        "X-Shopback-Agent": "sbconsumeragent/1.0",
        "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210",
        "X-Shopback-Store-Service": "true"
    }
    payload = {
        "accountId": 2464051,
        "browserName": "Chrome",
        "browserPlatform": "Android",
        "browserVersion": "71.0.3578.98",
        "ipaddress": "202.39.237.203",
        "mobileDevice": "Orca test cashback",
        "entryUrl": "localhost:3000",
        "dateCreated": 0
    }
    l.client.post(endpoint, json=(payload), name="web redirect v2",
                  headers=headers, catch_response=False)


class MatchAllSet(TaskSet):
    tasks = {redirect_test: 1}


class WebsiteUser(HttpLocust):
    task_set = MatchAllSet
    min_wait = 1000
    max_wait = 2000
