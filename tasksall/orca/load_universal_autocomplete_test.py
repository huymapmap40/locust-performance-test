# coding=UTF-8
import csv, random
from os.path import join, dirname
from locust import HttpUser, TaskSet, task, between

def read_csv(file_name):
    file_path = join(dirname(__file__), file_name)
    with open(file_path, 'r') as f:
        return list(csv.reader(f, delimiter=','))

CSV_FILE = "universal-autocomplete-en.csv"

class UniversalTasks(TaskSet):

    def __init__(self, parent):
        super(UniversalTasks, self).__init__(parent)
        self.headers = {
            "X-Shopback-Agent": "sbiosagent/3.30.0",
            "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
            "cf-connecting-ip": "10.201.7.16"
        }
        self.keywords = read_csv(CSV_FILE)

    @task
    def search(self):
        lat = '1.2770321'
        lon = '103.8458774'
        isIncludeTrendingOffers = 1
        keyword = random.choice(self.keywords)
        self.client.get(
            url="/autocomplete?inStoreLat={}&inStoreLon={}&includeTrendingOffers={}&keyword={}".format(
                lat, lon, isIncludeTrendingOffers, keyword),
            headers=self.headers, 
            name="/autocomplete"
        )
        self.client.close()

class WebsiteUser(HttpUser):
    tasks = [UniversalTasks,]
    wait_time = between(1, 3)
