from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.headers = {
            'Host': 'www.shopback.ph'
        }

    @task
    def main(self):
        url = "/"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def travelDeals(self):
        url = "/travel-deals"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def foodFestival(self):
        url = "/food-festival"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def healthBeautySale(self):
        url = "/health-beauty-sale"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def allStores(self):
        url = "/all-stores"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def techSale(self):
        url = "/tech-sale"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def referralInvite(self):
        url = "/referral/invite"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

    @task
    def howItWorks(self):
        url = "/how-it-works"
        response = self.client.get(url,verify=True,headers=self.headers)
        print("URL: " + url +" - Response Status: " + str(response.status_code))

class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
