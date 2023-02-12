from locust import HttpUser, task


class OnlineOrderWarmUpUser(HttpUser):
    merchant_service = None
    consumer_service = None
    core_service = None

    def on_start(self):
        self.merchant_service = f"https://{self.host}-merchant-service.testenv-hoolah.co"
        self.consumer_service = f"https://{self.host}-consumer-service.testenv-hoolah.co"
        self.core_service = f"https://{self.host}-core-service.testenv-hoolah.co"

    @task
    def warm_up_merchant_service(self):
        self.client.get(
            f"{self.merchant_service}/version",
            name="Warm Up Merchant Service",
        )

    @task
    def warm_up_consumer_service(self):
        self.client.get(
            f"{self.consumer_service}/version",
            name="Warm Up Consumer Service",
        )

    @task
    def warm_up_core_service(self):
        self.client.get(
            f"{self.core_service}/version",
            name="Warm Up Core Service",
        )
