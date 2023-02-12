import csv, random
from locust import HttpLocust, TaskSet

# Get keyword from query log
# curl --location --request GET 'http://internal-prod-au-orca-es7-XXXXXX.ap-southeast-2.elb.amazonaws.com:9200/au-product-query-log-2021-06/_search' --header 'Authorization: Basic XXXX' --header 'Content-Type: application/json' --data-raw '{
#     "size": 0,
#         "query": {
#         "bool": {
#             "must": [{
#                 "range": {
#                     "createdAt": {
#                         "from": "2021-06-01",
#                         "to": "2021-06-10"
#                     }
#                 }
#             }]
#         }
#     },
#     "aggs": {
#         "top": {
#             "terms": {
#                 "field": "name.keyword",
#                 "size": 1000
#             }
#         }
#     }
# }' | jq | grep key | sed 's/          "key": "//' | sed 's/",//' > auto-complete-keyword

def readCSV(fileName):
    with open(fileName, 'r') as f:
        r = csv.reader(f, delimiter=',')
        # next(r)  # skip header line
        return list(r)

keywords = readCSV("/locust-tasks/orca-autocomplete-tw.csv")
# keywords = readCSV("/locust-tasks/orca-autocomplete-au.csv")

def search(l):
    keyword = random.choice(keywords)
    url = "/search/keyword?types[]=category&types[]=product&value=%s" %(keyword[0])

    headers={"X-Shopback-Agent": "sbiosagent", "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3"}
    l.client.get(url, headers=headers, name="/search/keyword")


class UserBehavior(TaskSet):
     tasks = {search:1}

class WebsiteUser(HttpLocust):
        task_set = UserBehavior
        min_wait = 1000
        max_wait = 1000
