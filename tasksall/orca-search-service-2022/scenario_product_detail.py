from locust import TaskSet
import common
import random

# Get product ids
# curl --location --request GET 'http://internal-staging-au-orca-es7-XXXXXXX.ap-southeast-1.elb.amazonaws.com:9200/au-orca-product/_search' \
# --header 'Authorization: Basic XXXXX' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "size": 0,
#     "query": {
#         "bool": {
#             "filter": [
#                 {
#                     "range": {
#                         "offerCount": {
#                             "gt": 1
#                         }
#                     }
#                 }
#             ]
#         }
#     },
#     "aggs": {
#         "groupId": {
#             "terms": {
#                 "field": "groupId",
#                 "size": 1000
#             }
#         }
#     }
# }' | jq | grep key | sed 's/          "key": "//' | sed 's/",//' > product_ids_au.csv

ids = common.readCSV("/locust-tasks/fixtures_product_ids_%s.csv" % (common.COUNTRY.lower()))
class ProductDetailScenario(TaskSet):
    def task(self):
        name = '/search/product/:id/offer'
        id = random.choice(ids)
        url = '/search/product/%s/offer' %(id[0])
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)