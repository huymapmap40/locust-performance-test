from fixture_generator import FixtureGenerator
import os

HOSTS = {
    'au': 'http://internal-staging-au-orca-es7-1191401129.ap-southeast-1.elb.amazonaws.com:9200',
    'tw': 'http://internal-staging-tw-orca-es7-260874935.ap-southeast-1.elb.amazonaws.com:9200',
    'id': 'http://internal-staging-id-orca-es7-94940302.ap-southeast-1.elb.amazonaws.com:9200',
    'sg': 'http://internal-staging-sg-orca-es7-1167446581.ap-southeast-1.elb.amazonaws.com:9200',
    'my': 'http://internal-staging-my-orca-es7-iprice-608749183.ap-southeast-1.elb.amazonaws.com:9200'
}

data_generator = FixtureGenerator(
    HOSTS['au'],
    '<acc>',
    '<pwd>')


# Query without aggs
#data = data_generator.search('au-orca-product')          
#data_generator.write_collection_data_to_csv(
#    data,
#    'hits.hits',
#    '_id',
#    os.path.dirname(os.path.abspath(__file__)) + '/../fixtures/product_offer_ids_au.csv', False)

# Query with aggs
aggs = {
    "top": {
        "terms": {
            "field": "name.keyword",
            "size": 500
            }
        }
    }
data = data_generator.search('au-product-query-log-2022-06', aggs=aggs)
data_generator.write_collection_data_to_csv(
    data,
    'aggregations.top.buckets',
    'key',
    os.path.dirname(os.path.abspath(__file__)) + '/../fixtures/test_au.csv', False)
            
