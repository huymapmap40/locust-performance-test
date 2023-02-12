import urllib.parse

from locust import TaskSet
import json

IOS_HEADERS = {
    'Authorization': '',
    'Content-Type': 'application/json',
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-ShopBack-Build": "1",
    "X-ShopBack-Domain": "www.shopback.sg"
}
WEB_HEADERS = {
    'Authorization': '',
    'Content-Type': 'application/json',
    "X-Shopback-Agent": "sbconsumeragent/1.0",
    "X-ShopBack-Domain": "www.shopback.sg"
}

# we can only test content-service without content-system since locust only calls one service at a time
class TestBase(TaskSet):
    def __init__(self, parent, **kwargs):
        super(TestBase, self).__init__(parent)

        self.headers = kwargs['headers']

    def set_headers(self, headers):
        self.headers = headers

    def get(self, url):
        return self.client.get(
            url=url,
            headers=self.headers,
        )

    def load_component_content(self, component_id):
        url = "/v1.1/components/{id}/content?lon=103.94377184814185&lat=1.3795526261596807".format(id=component_id)
        return self.get(url=url)
    
    def load_banner_content(self, component_id):
        url = "/v1.1/components/{id}/content/banner-set?lon=103.94377184814185&lat=1.3795526261596807".format(id=component_id)
        return self.get(url=url)

    def load_see_more_component_content(self, component_id, page=None):
        url = "/v1.1/components/{id}/content/see-more?page={page}&lon=103.94377184814185&lat=1.3795526261596807".format(id=component_id, page=page)
        return self.get(url=url)
    
    def load_dynamic_content(self, component_map_id, entity_ids):
        entity_ids_string = json.dumps(entity_ids)
        url = "/v1.1/components/dynamic/{component_map_id}?position=0&page_track_meta_model_name=load-test&page_track_meta_model_version=load-test&page_track_meta_track_id=0&curation_id=0&curation_name=test&entityIds={entity_ids_string}&title=load-test".format(component_map_id=component_map_id, entity_ids_string=entity_ids_string)
        return self.get(url=url)


class AppTestBase(TestBase):
    def __init__(self, parent):
        super(AppTestBase, self).__init__(parent, headers=IOS_HEADERS)


class WebTestBase(TestBase):
    def __init__(self, parent):
        super(WebTestBase, self).__init__(parent, headers=WEB_HEADERS)
