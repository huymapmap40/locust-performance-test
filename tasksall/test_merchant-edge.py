from locust import HttpUser, TaskSet, task, between
import random
import json


class UserBehavior(TaskSet):
    @task
    class SwordfishSet(TaskSet):
        def __init__(self, parent):
            super().__init__(parent)
            self.headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Shopback-Agent': 'sbstingray/1.0',
                'X-Shopback-Token': '070fe3aecc3f7fdb9756690fd8d4ec58',
                'X-Shopback-Admin': 'Merchant Edge',
            }
            self.storeIds = [38, 40, 49, 59, 60, 64, 68, 81, 93, 102, 155, 169, 258, 271, 289, 294, 318, 326, 330, 332, 388, 432, 440, 491, 501]
            self.storeId = random.choice(self.storeIds)
            
        @task
        def getStoreDeal(self):
            with self.client.get(
                url='/adm/stores/'+ str(self.storeId) +'/deals',
                headers=self.headers,
                catch_response=True
            ) as response:
                res = json.loads(response.text)
                if res.get('data')['message'] == 'Please use Needle instead':
                    response.success()


        @task
        def getStoreOffer(self):
            with self.client.get(
                url='/adm/stores/'+ str(self.storeId) +'/offers',
                headers=self.headers,
                catch_response=True
            ) as response:
                res = json.loads(response.text)
                if res.get('data')['message'] == 'Please use Needle instead':
                    response.success()

        @task
        def getStoreOffer(self):
            with self.client.get(
                url='/adm/stores/'+ str(self.storeId) +'/offers',
                headers=self.headers,
                catch_response=True
            ) as response:
                res = json.loads(response.text)
                if res.get('data')['message'] == 'Please use Needle instead':
                    response.success()

        @task
        def getStoreAvailableOffer(self):
            with self.client.get(
                url='/adm/stores/'+ str(self.storeId) +'/availableoffers',
                headers=self.headers,
                catch_response=True
            ) as response:
                res = json.loads(response.text)

                if res.get('data')['message'] == 'Please use Needle instead':
                    response.success()

        @task
        def getStoreSelectedOffer(self):
            with self.client.get(
                url='/adm/stores/'+ str(self.storeId) +'/selectedoffers',
                headers=self.headers,
                catch_response=True
            ) as response:
                res = json.loads(response.text)
                if res.get('data')['message'] == 'Please use Needle instead':
                    response.success()
    @task
    class InternalDealSet(TaskSet):
        def __init__(self, parent):
            super().__init__(parent)
            
        
        def on_start(self):
            if hasattr(self, 'deals'):
                return
            dealsResponse = self.client.get(
                url='/v1/internal/deals',
            )
            self.deals = json.loads(dealsResponse.text)
            self.deal = random.choice(self.deals.get('data'))

        @task
        def getInternalDeals(self):
            self.client.get(
                url='/v1/internal/deals',
            )

        @task
        def getInternalDeal(self):
            deal_id = self.deal.get('id')
            self.client.get(
                url='/v1/internal/deals/' + str(deal_id),
            )

    @task
    class ExternalDealSet(TaskSet):
        def __init__(self, parent):
            super().__init__(parent)
            self.headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Shopback-Agent': 'sbconsumeragent/1.0',
                'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
            }
            self.merchantIds = [11086, 11305, 11088,11089, 11091, 11093,11306, 11094, 11096,11097, 11307, 11099,11100, 11308, 11101,11102, 11103, 11104,11105]
            self.merchantId = random.choice(self.merchantIds)


        @task
        def getExternalMerchantDeals(self):
            self.client.get(
                url='/v1/merchants/'+ str(self.merchantId) +'/deals',
                headers=self.headers
            )

        @task
        def getExternalMerchantExpiredDeals(self):
            self.client.get(
                url='/v1/merchants/'+ str(self.merchantId) +'/deals/expired',
                headers=self.headers
            )

    @task
    class ProductSet(TaskSet):
        def __init__(self, parent):
            super().__init__(parent)

            self.headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Shopback-Agent': 'sbconsumeragent/1.0',
                'X-Shopback-Internal': '682a46b19b953306c9ee2e8deb0dc210'
            }
            
        
        def on_start(self):
            if not hasattr(self, 'categories'):
                categoriesResponse = self.client.get(
                    url='/product/v1/categories',
                )
                self.categories = json.loads(categoriesResponse.text)
                self.category = random.choice(self.categories.get('data'))

            if not hasattr(self, 'signals'):
                signalsResponse = self.client.get(
                    url='/product/v1/signals',
                )
                self.signals = json.loads(signalsResponse.text)
                self.signal = random.choice(self.signals.get('data'))

            

        @task
        def getCategories(self):
            self.client.get(
                url='/product/v1/categories',
            )

        @task
        def getSignals(self):
            self.client.get(
                url='/product/v1/signals',
            )

        @task
        def getAvailableCategories(self):
            self.client.get(
                url='/product/v1/categories/available',
            )

        @task
        def getSignalDetail(self):
            signal_id = self.signal.get('id')
            self.client.get(
                url='/product/v1/signals/' + str(signal_id),
            )

        @task
        def getAvailableCategoriesProducts(self):
            category_id = self.category.get('id')
            self.client.get(
                url='/product/v1/categories/' + str(category_id) + '/products/available',
                headers=self.headers,
            )

        @task
        def getAvailableSignalsProducts(self):
            signal_id = self.signal.get('id')
            self.client.get(
                url='/product/v1/signals/' + str(signal_id) + '/products/available',
                headers=self.headers,
            )


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    wait_time = between(10, 50)
