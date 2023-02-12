from random import randint, choice
from locust import HttpUser, between, tag, task
from base import AppTestBase
from users import personalized_testing_users
from users_utility import get_user_auth_header
import logging

class TestApp(AppTestBase):
    def on_start(self):
        super(TestApp, self).on_start()

    @task(1)
    def test_home_personalized(self):
        components_loaded = 20
        user = choice(personalized_testing_users)

        # use a random device id to bypass the controller level memoization
        self.headers['x-device-id'] = "Device Id:{deviceId}".format(deviceId=randint(1, 120000000))

        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        # logging.info("Authorization: {auth}".format(auth=self.headers['Authorization']))
        self.load_page('home', 'loadtest2022', components_loaded)

class User(HttpUser):
    tasks = [TestApp]
    wait_time = between(0.5, 1.5)
