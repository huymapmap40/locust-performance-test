from locust import TaskSet
import common
import random

# Get related keywords from user in amplitude
# https://docs.google.com/spreadsheets/d/1rGwAo_FLxyDThh1BCBj3BshdJw5QJsHeIJg3QFnHGCY/edit#gid=855212874

keywords = common.readCSV("/locust-tasks/fixtures_voucher_%s.csv" % (common.COUNTRY.lower()))
class SearchVoucherScenario(TaskSet):
    def task(self):
        name = '/search/voucher'
        keyword = random.choice(keywords)
        url = '/search/voucher?name=%s' %(keyword[0])
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)