from locust import HttpUser, TaskSet, task, between

DEFAULT_HEADERS = {
    'Content-Type': 'application/json'
}


class GetStores(TaskSet):
    weight = 5

    def get_stores(self, ver='v3', params=None):
        url = f'/api/{ver}/stores'

        params_suffix = f' {repr(params)}' if params else ''
        self.client.get(
            url=url,
            headers=DEFAULT_HEADERS,
            params=params,
            name=f'Get api/stores {ver}{params_suffix}'
        )

    @task(5)
    def get_stores_v3(self):
        self.get_stores('v3')

    @task(1)
    def get_stores_v3_with_top(self):
        self.get_stores('v3', {'top': 'true'})

    wait_time = between(0.5, 10)

class GetSettings(TaskSet):
    weight = 1

    @task
    def get_settings_v2(self, ver='v2'):
        url = f'/api/{ver}/settings'

        self.client.get(
            url=url,
            headers=DEFAULT_HEADERS,
            name=f'Get settings {ver}'
        )

    wait_time = between(0.5, 10)


class WebsiteUser(HttpUser):
    tasks = [GetStores, GetSettings]
