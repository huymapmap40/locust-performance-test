# coding=UTF-8
import csv
import random
from locust import HttpUser, TaskSet, task, between
from os.path import join, dirname
from urllib.parse import quote


def read_csv(file_name):
    file_path = join(dirname(__file__), file_name)
    with open(file_path, 'r') as f:
        return list(csv.reader(f, delimiter=','))


CSV_FILE = "orca-au-prod-qlog.csv"


class MerchantSpellerTasks(TaskSet):

    def __init__(self, parent):
        super(MerchantSpellerTasks, self).__init__(parent)
        self.headers = {
            "X-Shopback-Agent": "sbiosagent/3.30.0",
            "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        }
        self.queries = read_csv(CSV_FILE)

    @task
    def search(self):
        query = random.choice(self.queries)[0]
        self.client.get(
            url="/merchantSpellCorrect?market={}&query={}".format('au', quote(query)),
            headers=self.headers,
            name="/merchantSpellCorrect"
        )


class WebsiteUser(HttpUser):
    tasks = [MerchantSpellerTasks, ]
    wait_time = between(1, 1)
