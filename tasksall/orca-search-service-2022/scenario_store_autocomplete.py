from locust import TaskSet
import common
import random

keywords = common.readCSV("/locust-tasks/fixtures_store_keyword_%s.csv" % (common.COUNTRY.lower()))
class StoreAutocompleteScenario(TaskSet):
    def task(self):
        name = '/search/keyword/store'
        keyword = random.choice(keywords)
        url = '/search/keyword/store?value=%s' %(keyword[0])
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)