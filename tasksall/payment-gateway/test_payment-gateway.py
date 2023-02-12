from typing import Dict
from locust import TaskSet, HttpUser, task, between
from uuid import uuid4
from utility_users import get_unique_account_id

def get_payment_method(locustUser: HttpUser, headers: Dict[str, str], account_id: int) -> Dict[str, str]:
    res = locustUser.client.get(
            url="/payment-methods?buildNumber=3800099&accountId=" + str(account_id),
            headers=headers,
            name="/payment-methods"
        )
    response_body = res.json()
    res.close()

    if (
        "data" not in response_body
        or "card" not in response_body["data"]
        or "params" not in response_body["data"]["card"][0]
    ):
        raise RuntimeError(f"Invalid payment methods response: {response_body}")

    return response_body["data"]["card"][0]["params"]

class AppBehaviour(TaskSet):
    account_id: int = 0
    headers: Dict[str, str] = {
        'X-Api-Key': '43b9bc57-a003-41b6-a8c1-8cce56650df3'
    }
    payment_method_params: Dict[str, str] = {} 
    

    def on_start(self) -> None:
        self.account_id = get_unique_account_id()
        self.payment_method_params = get_payment_method(self, self.headers, self.account_id)

    @task(20)
    def get_available_cashback(self) -> None:
        res = self.client.get(
            url="/payment-methods/available-cashback?accountId=" + str(self.account_id),
            headers=self.headers,
            name="/payment-methods/available-cashback"
        )
        # print("Available cashback", res.json())
        res.close()

    @task(20)
    def get_last_used_payment_method(self) -> None:
        res = self.client.get(
            url="/payment-methods/last-used?accountId=" + str(self.account_id),
            headers=self.headers,
            name="/payment-methods/last-used"
        )
        # print("Last used payment method", res.json())
        res.close()

    @task(10)
    def get_available_payment_methods(self) -> None:
        res = self.client.get(
            url="/payment-methods?buildNumber=3800099&accountId=" + str(self.account_id),
            headers=self.headers,
            name="/payment-methods"
        )
        # print("Available payment methods", res.json())
        res.close()

    @task(4)
    def make_payment_card(self) -> None:
        payload = {
            "accountId": self.account_id,
            "amount": 500,
            "paymentMethods": [
                {
                    "type": "card",
                    "category": "card",
                    "amount": 500,
                    "params": self.payment_method_params
                }
            ],
            "category": "Digital Goods",
            "referenceNumber": str(uuid4()),
            "idempotentId": str(uuid4()),
            "connectionInformation": {
                "agent": "ShopBack/3.17.0 (com.shopback.app; build:3170099; Android 10; RMX1931 realme RMX1931L1) okhttp/4.9.0",
                "build": "3460000",
                "clientUserAgent": "a123c9d2310b371b",
                "cfConnectingIp": "127.0.0.1",
                "cfPseudoIpv4": "127.0.0.1",
                "forwardedFor": "127.0.0.1",
                "originalForwardedFor": "127.0.0.1",
                "realIp": "127.0.0.1",
                "deviceId": "a123c9d2310b371b",
                "deviceModel": "Android",
                "uid": str(uuid4()),
            },
            "purchaseItems": [
                {
                    "name": "LOAD_TEST_ITEM",
                    "quantity": 1,
                    "price": 500,
                    "itemId": "1",
                    "brand": "LOAD_TEST_BRAND"
                }
            ]
        }

        res = self.client.post(
            url='/payments',
            headers=self.headers,
            json=payload
        )
        # print("Card payment:", res.status_code ,res.json())
        res.close()

    @task(2)
    def make_payment_card_forter(self) -> None:
        payload = {
            "accountId": self.account_id,
            "amount": 5000,
            "paymentMethods": [
                {
                    "type": "card",
                    "category": "card",
                    "amount": 5000,
                    "params": self.payment_method_params
                }
            ],
            "category": "Digital Goods",
            "referenceNumber": str(uuid4()),
            "idempotentId": str(uuid4()),
            "connectionInformation": {
                "agent": "ShopBack/3.17.0 (com.shopback.app; build:3170099; Android 10; RMX1931 realme RMX1931L1) okhttp/4.9.0",
                "build": "3460000",
                "clientUserAgent": "a123c9d2310b371b",
                "cfConnectingIp": "127.0.0.1",
                "cfPseudoIpv4": "127.0.0.1",
                "forwardedFor": "127.0.0.1",
                "originalForwardedFor": "127.0.0.1",
                "realIp": "127.0.0.1",
                "deviceId": "a123c9d2310b371b",
                "deviceModel": "Android",
                "uid": str(uuid4()),
            },
            "purchaseItems": [
                {
                    "name": "LOAD_TEST_ITEM",
                    "quantity": 1,
                    "price": 500,
                    "itemId": "1",
                    "brand": "LOAD_TEST_BRAND"
                }
            ]
        }

        res = self.client.post(
            url='/payments',
            headers=self.headers,
            json=payload,
            name="/payments (card)"
        )
        # print("Card payment Forter:", res.status_code ,res.json())
        res.close()

    @task(1)
    def make_payment_cashback(self) -> None:
        payload = {
            "accountId": self.account_id,
            "amount": 500,
            "paymentMethods": [
                {
                    "type": "cashback",
                    "category": "cashback",
                    "amount": 500
                }
            ],
            "category": "Digital Goods",
            "referenceNumber": str(uuid4()),
            "idempotentId": str(uuid4()),
            "connectionInformation": {
                "agent": "ShopBack/3.17.0 (com.shopback.app; build:3170099; Android 10; RMX1931 realme RMX1931L1) okhttp/4.9.0",
                "build": "3460000",
                "clientUserAgent": "a123c9d2310b371b",
                "cfConnectingIp": "127.0.0.1",
                "cfPseudoIpv4": "127.0.0.1",
                "forwardedFor": "127.0.0.1",
                "originalForwardedFor": "127.0.0.1",
                "realIp": "127.0.0.1",
                "deviceId": "a123c9d2310b371b",
                "deviceModel": "Android",
                "uid": str(uuid4()),
            },
            "purchaseItems": [
                {
                    "name": "LOAD_TEST_ITEM",
                    "quantity": 1,
                    "price": 500,
                    "itemId": "1",
                    "brand": "LOAD_TEST_BRAND"
                }
            ]
        }

        res = self.client.post(
            url='/payments',
            headers=self.headers,
            json=payload,
            name="/payments (cashback)"
        )
        # print("Cashback payment:", res.status_code ,res.json())
        res.close()

    @task(2)
    def make_payment_split(self) -> None:
        payload = {
            "accountId": self.account_id,
            "amount": 500,
            "paymentMethods": [
                {
                    "type": "card",
                    "category": "card",
                    "amount": 400,
                    "params": self.payment_method_params
                },
                {
                    "type": "cashback",
                    "category": "cashback",
                    "amount": 100
                }
            ],
            "category": "Digital Goods",
            "referenceNumber": str(uuid4()),
            "idempotentId": str(uuid4()),
            "connectionInformation": {
                "agent": "ShopBack/3.17.0 (com.shopback.app; build:3170099; Android 10; RMX1931 realme RMX1931L1) okhttp/4.9.0",
                "build": "3460000",
                "clientUserAgent": "a123c9d2310b371b",
                "cfConnectingIp": "127.0.0.1",
                "cfPseudoIpv4": "127.0.0.1",
                "forwardedFor": "127.0.0.1",
                "originalForwardedFor": "127.0.0.1",
                "realIp": "127.0.0.1",
                "deviceId": "a123c9d2310b371b",
                "deviceModel": "Android",
                "uid": str(uuid4()),
            },
            "purchaseItems": [
                {
                    "name": "LOAD_TEST_ITEM",
                    "quantity": 1,
                    "price": 500,
                    "itemId": "1",
                    "brand": "LOAD_TEST_BRAND"
                }
            ]
        }

        res = self.client.post(
            url='/payments',
            headers=self.headers,
            json=payload,
            name="/payments (split)"
        )
        # print("Split payment:", res.status_code ,res.json())
        res.close()


class PaymentGatewayApp(HttpUser):
    wait_time = between(3, 7)
    tasks = [AppBehaviour]
