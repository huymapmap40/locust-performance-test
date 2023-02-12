from random import randint

from locust import HttpUser, between, tag, task

from content_system_base import AppTestBase, WebTestBase

class CotentSystemTestApp(AppTestBase):
    def on_start(self):
        super(CotentSystemTestApp, self).on_start()

    @task(80)
    def test_home_screen(self):
        components_loaded = 20
        self.load_page('home', 'sboc', components_loaded)

    @task(40)
    def test_campaign_screen(self):
        components_loaded = 20
        self.load_page('campaign', 'premium_brands', components_loaded)

class ContentSystemTestWeb(WebTestBase):
    def on_start(self):
        super(ContentSystemTestWeb, self).on_start()

    @task(20)
    def test_home_page(self):
        components_loaded = 3
        self.load_page('home', '/homepage-cs20-live', components_loaded)

class ContentSystemUser(HttpUser):
    tasks = [CotentSystemTestApp, ContentSystemTestWeb]
    wait_time = between(0.5, 1.5)
