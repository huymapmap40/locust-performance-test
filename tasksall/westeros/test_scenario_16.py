from locust import task, tag, TaskSet
import common


class Scenario16(TaskSet):
    def __init__(self, parent):
        super(Scenario16, self).__init__(parent)
        self.search_keyword = 'Xiaomi'
        self.cookies = common.COOKIES

    @tag('scenario16')
    @task
    def task16(self):
        self.client.get(url=f'{common.BASE_URL}/',
                        cookies=self.cookies,
                        headers=common.HEADERS,
                        name='Scenario16 - /')

        self.client.get(url=f'{common.BASE_URL}/wes-api/orca/search?keyword={self.search_keyword}',
                        headers=common.HEADERS,
                        cookies=self.cookies,
                        name=f'Scenario16 - /wes-api/orca/search?keyword={self.search_keyword}')
                        
        self.client.get(
            url=f'{common.BASE_URL}/product/compare/Xiaomi-Mi-A3/o1.p10.69a18af980b09c7e959f9d2db14f5554c59e6758?q=Xiaomi',
            cookies=self.cookies,
            headers=common.HEADERS, name='Scenario16 - /product/compare/')

        self.client.get(
            url=f'{common.BASE_URL}/wes-api/orca/product/api/product/qoo10%3A534809823/price-history',
            cookies=self.cookies,
            headers=common.HEADERS, name=f'Scenario16 - /wes-api/orca/product/api/product/')

        self.client.get(url=f'{common.BASE_URL}/product/redirect/plink/qoo10%3A534809823?storeId=18708',
                        cookies=self.cookies,
                        headers=common.HEADERS, name=f'Scenario16 - /product/redirect/plink/')
