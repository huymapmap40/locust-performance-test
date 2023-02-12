import urllib.parse

from locust import TaskSet

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

BASE_URL = 'http://content-system.production-sg.svc.cluster.local'

class TestBase(TaskSet):
    def __init__(self, parent, **kwargs):
        super(TestBase, self).__init__(parent)

        self.headers = kwargs['headers']

    def set_headers(self, headers):
        self.headers = headers

    def load_layout(self, page_type, identifier):
        identifier = urllib.parse.quote(identifier, safe='')

        url = "{baseUrl}/v1/layouts/{type}/{identifier}".format(baseUrl=BASE_URL, type=page_type, identifier=identifier)
        return self.get(url=url)

    def get(self, url):
        return self.client.get(
            url=url,
            headers=self.headers
        )

    def load_component_content(self, component_id):
        url = "{baseUrl}/v1/components/{id}/content".format(baseUrl=BASE_URL, id=component_id)
        return self.get(url=url)

    def load_see_more_component_content(self, component_id, page=None):
        url = "{baseUrl}/v1/components/{id}/content/see-more?page={page}".format(baseUrl=BASE_URL, id=component_id, page=page)
        return self.get(url=url)

    def load_page(self, page_type, identifier, components_loaded=3):
        response = self.load_layout(page_type, identifier)
        if response.status_code == 200:
            json_data = response.json()
            if len(json_data['data']['components']) < components_loaded:
                components_loaded = len(json_data['data']['components'])
            for i in range(0, components_loaded):
                component = json_data['data']['components'][i]
                if 'contentUrl' in component['detail']:
                    url = "{baseUrl}{url}".format(baseUrl=BASE_URL,url=component['detail']['contentUrl'])
                    self.get(url=url)


class AppTestBase(TestBase):
    def __init__(self, parent):
        super(AppTestBase, self).__init__(parent, headers=IOS_HEADERS)


class WebTestBase(TestBase):
    def __init__(self, parent):
        super(WebTestBase, self).__init__(parent, headers=WEB_HEADERS)
