import time
import uuid
from locust import HttpUser, task


class OnlineOrderCheckoutUser(HttpUser):
    username = "change-it"
    password = "change-it"

    merchant_service = None
    consumer_service = None
    authorization_header = None

    order_uuid = None
    order_context_token = None
    order_context_token_used = False

    def on_stop(self):
        self.client.post(
            f"{self.merchant_service}/auth/logout",
            headers={
                "Authorization": self.authorization_header,
            },
            name="Merchant API User Logout",
        )

    def on_start(self):
        self.merchant_service = f"https://{self.host}-merchant-service.testenv-hoolah.co"
        self.consumer_service = f"https://{self.host}-consumer-service.testenv-hoolah.co"
        res = self.client.post(
            f"{self.merchant_service}/auth/login",
            headers={
                "Hoolah-User-Type": "MERCHANT",
            },
            json={
                "username": self.username,
                "password": self.password
            },
            name="Merchant API User Login",
        )
        bearer_token = res.json()["token"]
        self.authorization_header = f"Bearer {bearer_token}"

    @task(1)
    def initiate_online_order(self):
        res = self.client.post(
            f"{self.merchant_service}/order/initiate",
            headers={
                "Authorization": self.authorization_header,
            },
            json={
                "totalAmount": 123.45,
                "originalAmount": 123.45,
                "consumerEmail": f"{str(uuid.uuid4())}@fake.user",
                "consumerFirstName": "First",
                "consumerLastName": "Last",
                "currency": "SGD",
                "shippingAddress": {
                    "countryCode": "SG",
                    "line1": "line1",
                },
                "billingAddress": {
                    "countryCode": "SG",
                    "line1": "line1",
                },
                "items": [
                    {
                        "name": "fake",
                        "quantity": 1,
                        "sku": "fake",
                        "description": "fake",
                    },
                ]
            },
            name="Initiate Online Order",
        )

        self.order_uuid = res.json()["orderUuid"]
        self.order_context_token = res.json()["orderContextToken"]
        self.order_context_token_used = False

    @task(1)
    def display_landing_page_by_order_context_token(self):
        if self.order_context_token:

            self.client.get(
                f"{self.consumer_service}/order/country?orderContextToken={self.order_context_token}",
                name="Get Order Country by Order Context Token",
            )

            self.client.post(
                f"{self.consumer_service}/order/checkout?platform=MERCHANT_IN_APP_WEB&orderContextToken={self.order_context_token}",
                name="Track Checkout Platform by Order Context Token",
            )

            if not self.order_context_token_used:
                self.client.get(
                    f"{self.consumer_service}/order/order-context/{self.order_context_token}",
                    name="Get Order Details by Order Context Token",
                )
                self.order_context_token_used = True

            for _ in range(10):
                self.client.get(
                    f"{self.consumer_service}/order/status?orderContextToken={self.order_context_token}",
                    name="Poll Order Status by Order Context Token",
                )
                time.sleep(5.0)

    @task(3)
    def get_online_order_info_by_order_uuid(self):
        if self.order_uuid:
            self.client.get(
                f"{self.merchant_service}/order/{self.order_uuid}",
                headers={
                    "Authorization": self.authorization_header,
                },
                name="Get Order Info by Order UUID",
            )
