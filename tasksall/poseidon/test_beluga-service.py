from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    """Mapping data, depends on the DEV's database.
        merchantMap = {
            pchome: 2227,
            shopee: 2281,
            agoda: 838,
            booking: 318
        }
        categoryMap = {
            flights: 1,
            accommodation: 2,
            tours: 3,
            car_rental: 4,
            travel_insurance: 5
        }
    """
    _headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    _url = '/beluga/recommendation/merchants'

    def _get_recommendations(self, query_string=''):
        self.client.get(
            f'{self._url}?{query_string}',
            headers=self._headers,
            name='Get Recommendations from API')

    @task
    def query_with_pchome(self):
        self._get_recommendations('?merchantId=2227&categoryId=0')

    @task
    def query_with_shopee(self):
        self._get_recommendations('?merchantId=2281&categoryId=0')

    @task
    def query_with_agoda_flights(self):
        self._get_recommendations('?merchantId=838&categoryId=1')

    @task
    def query_with_agoda_accommodation(self):
        self._get_recommendations('?merchantId=838&categoryId=2')

    @task
    def query_with_booking(self):
        self._get_recommendations('?merchantId=318&categoryId=2')


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
