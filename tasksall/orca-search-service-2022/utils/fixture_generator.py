import csv
import random
from collections.abc import MutableMapping
import json
from elasticsearch import Elasticsearch
import base64

class FixtureGenerator:
    
    def __init__(self, es_host, es_acc, es_pwd):
        basic_auth = base64.b64encode('{}:{}'.format(es_acc, es_pwd).encode('ascii'))
        self.client = Elasticsearch(es_host, basic_auth=basic_auth)
        
    def search(self, index, query=None, aggs=None, size=1000):
        if not query:
            query = { "match_all": {} }
        return self.client.search(index=index, query=query, size=size, from_=random.randint(1, 10000), aggs=aggs)
    
    def write_collection_data_to_csv(self, es_query_result, collection_path, target_path_relative_to_collection, output_file_path, random_length_of_target_value = False):
        """This function is used to write collection data of es_query_result into csv file
        For example, es_query_result would be like
        {
            "took" : 4,
            "timed_out" : false,
            "_shards" : {
                "total" : 3,
                "successful" : 3,
                "skipped" : 0,
                "failed" : 0
            },
            "hits" : {
                "total" : {
                "value" : 10000,
                "relation" : "gte"
                },
                "max_score" : 1.0,
                "hits" : [
                {
                    "_index" : "tw-raw-product-data-2022-06-28",
                    "_type" : "_doc",
                    "_id" : "books:F010785029",
                    "_score" : 1.0,
                    "_source" : {
                    "title" : "The Newsbreaker",
                    "titleLength" : 15,
                    }
                }
                ]
            }
        }
        
        If you want write all titles to the csv, just call 
        
        write_hits_data_to_csv(es_query_result, 'hits.hits', '_source.title', output_file_path, random_length_of_target_value)


        Args:
            es_query_result (dict): query result from es api
            collection_path (str): collection path which is separate by dot. Like, 'hits.hits'.
            target_path_relative_to_collection (str): target path which is separate by dot(what you want to write into csv file) relative to collection path. Like, '_source.title'
            output_file_path (str): output file path
            random_length_of_target_value (bool, optional): random your target length from 0 to random int. Defaults to False.
        """
        f = open(output_file_path, 'w' , encoding='UTF8')

        # create the csv writer
        writer = csv.writer(f)
        for item in self._get_value_at_path(es_query_result, collection_path):
            target_value = self._get_value_at_path(item, target_path_relative_to_collection)
            keyword = [target_value[0: random.randint(0, len(target_value))].strip('"')] if random_length_of_target_value else [target_value.strip('"')]
            if (keyword):
                # write a row to the csv file
                writer.writerow(keyword)
        f.close()
        
    @staticmethod
    def _get_value_at_path(obj, path):
        *parts, last = path.split('.')

        for part in parts:
            if not part in obj:
                raise Exception('{} has no key: {} part'.format(part, json.dumps(obj)))
            obj = obj[part]

        return obj[last]