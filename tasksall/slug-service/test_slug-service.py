import urllib.parse
from locust import TaskSet, HttpUser, task, tag
from random import randint

class TestGetSlug(TaskSet):
    def __init__(self, parent, **kwargs):
        super(TestGetSlug, self).__init__(parent)

        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbconsumeragent/1.0',
            'X-ShopBack-Domain': 'www.shopback.sg'
        }

    def get_slug(self, slug):

        slug = urllib.parse.quote(slug, safe='')

        url = "/slugs/{slug}".format(slug=slug)
        return self.client.get(
            url=url,
            headers=self.headers
        )

    @tag('sboc1')
    @task
    def test_get_slug_sboc(self):
        return self.get_slug('sboc1')

    @tag('loadtest1')
    @task
    def test_get_slug_load_test(self):
        return self.get_slug('loadtest1')

class WebsiteUser(HttpUser):
    tasks =  [TestGetSlug]
    min_wait = 10
    max_wait = 30
