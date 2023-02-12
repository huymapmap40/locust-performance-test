from random import randint

from locust import HttpUser, between, tag, task

from base import AppTestBase, WebTestBase

class TestApp(AppTestBase):
    def on_start(self):
        super(TestApp, self).on_start()

    @task(100)
    def test_home_screen(self):
        components_loaded = 20

        # use a random device id to bypass the controller level memoization
        self.headers['x-device-id'] = "Device Id:{deviceId}".format(deviceId=randint(1, 120000000))

        self.load_page('home', 'sboc', components_loaded)

    @task(80)
    def test_campaign_screen(self):
        components_loaded = 20

        # use a random device id to bypass the controller level memoization
        self.headers['x-device-id'] = "Device Id:{deviceId}".format(deviceId=randint(1, 120000000))

        self.load_page('home', 'uhs', components_loaded)

class TestWeb(WebTestBase):
    def on_start(self):
        super(TestWeb, self).on_start()

    @task(20)
    def test_home_page(self):
        components_loaded = 20

        # use a random device id to bypass the controller level memoization
        self.headers['x-device-id'] = "Device Id:{deviceId}".format(deviceId=randint(1, 120000000))
        
        self.load_page('home', '/homepage-cs20-live', components_loaded)

class User(HttpUser):
    tasks = [TestApp, TestWeb]
    wait_time = between(0.5, 1.5)
