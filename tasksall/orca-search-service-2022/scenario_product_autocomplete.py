from locust import TaskSet
import common
import random

# Get keyword from production's query log
# curl --location --request GET 'http://internal-prod-tw-orca-es7-XXXXXX.ap-northeast-1.elb.amazonaws.com:9200/tw-product-query-log-2022-06/_search' \
# --header 'Authorization: Basic XXXXXX' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "size": 0,
#         "query": {
#         "bool": {
#             "must": [{
#                 "range": {
#                     "createdAt": {
#                         "from": "2022-06-20",
#                         "to": "2022-06-20"
#                     }
#                 }
#             }]
#         }
#     },
#     "aggs": {
#         "top": {
#             "terms": {
#                 "field": "name.keyword",
#                 "size": 500
#             }
#         }
#     }
# }' | jq | grep key | sed 's/          "key": "//' | sed 's/",//' > product_autocomplete_tw.csv

keywords = common.readCSV("/locust-tasks/fixtures_product_autocomplete_%s.csv" % (common.COUNTRY.lower()))
class ProductAutocompleteScenario(TaskSet):
    def task(self):
        name = '/search/keyword'
        keyword = random.choice(keywords)
        url = '/search/keyword?types[]=category&types[]=product&value=%s' %(keyword[0])
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
