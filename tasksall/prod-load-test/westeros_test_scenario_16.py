from locust import task, tag, TaskSet
import westeros_common


class Scenario16(TaskSet):
    def __init__(self, parent):
        super(Scenario16, self).__init__(parent)
        self.search_keyword = 'Xiaomi'
        self.cookies = westeros_common.COOKIES

    @tag('scenario16')
    @task
    def task16(self):
        self.client.get(url=f'{westeros_common.BASE_URL}/',
                        cookies=self.cookies,
                        headers=westeros_common.HEADERS,
                        name='Scenario16 - /')

        self.client.get(url=f'{westeros_common.BASE_URL}/wes-api/orca/product/api/store/search?keyword={self.search_keyword}',
                        headers=westeros_common.HEADERS,
                        cookies=self.cookies,
                        name=f'Scenario16 - /wes-api/orca/product/api/store/search?keyword={self.search_keyword}')
                        
        self.client.get(
            url=f'{westeros_common.BASE_URL}/product/compare/Xiaomi-Mi-A1/o1.p10.68d96bfbaf9bcdbec65ad55b6177615d876cc67e?q=Xiaomi',
            cookies=self.cookies,
            headers=westeros_common.HEADERS, name='Scenario16 - /product/compare/')

        self.client.get(
            url=f'{westeros_common.BASE_URL}/wes-api/orca/product/api/product/lazada%3A486858625_SGAMZ/price-history',
            cookies=self.cookies,
            headers=westeros_common.HEADERS, name=f'Scenario16 - /wes-api/orca/product/api/product/')
        # no need to run redirect
        # self.client.get(url=f'{westeros_commonBASE_URL}/product/redirect/plink/lazada%3A486858625_SGAMZ?storeId=19352',
        #                 cookies=self.cookies,
        #                 headers=common.HEADERS, name=f'Scenario16 - /product/redirect/plink/')