import common
from locust import TaskSet

# Only used in ID country
class MobilePowerscreenScenario(TaskSet):
    def task(self):
        name = '/mobile/powerscreen'
        url = '/mobile/powerscreen?type=store&storeId=17680'
        headers=common.HEADERS
        self.client.get(url, headers=headers, name=name)
