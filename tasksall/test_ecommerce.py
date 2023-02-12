from typing import Dict
import random
from uuid import uuid4
from locust import TaskSet, HttpUser, task, between
from utility_users import get_unique_email, get_unique_account_id, get_user_headers_by_login, get_user_headers_by_account_id


def get_payment_method(locustUser: HttpUser, headers: Dict[str, str]) -> str:
    res_get = locustUser.client.get(
        url="/ecommerce/mobile/payment-methods",
        headers=headers,
    )
    payment_methods = res_get.json()

    res_get.close()

    if (
        "data" not in payment_methods
        or "paymentMethods" not in payment_methods["data"]
        or not payment_methods["data"]["paymentMethods"]
        or "_id" not in payment_methods["data"]["paymentMethods"][0]
    ):
        raise RuntimeError(f"Unsuccessful response: {payment_methods}")

    payment_method = payment_methods["data"]["paymentMethods"][0]
    payment_method = payment_method and payment_method["_id"]

    return payment_method


class UserBehaviour(TaskSet):
    # email = ""
    # password = ""
    account_id = 0

    headers = {}
    payment_method = ""

    sku_read_codes = ["LOAD_TEST_UNLIMITED"] # pre-fill
    outlets = ["0060845"] # pre-fill
    sku_write_codes = ["LOAD_TEST_UNLIMITED"] # pre-fill
    sku_read_code = ""
    outlet = ""
    sku_write = {}
    cashback_to_pay = 100 # used for split orders, ensure < sku unitPrice

    def on_start(self) -> None:
        # self.email = get_unique_email()
        # self.password = "loadtest1111"
        self.account_id = get_unique_account_id()

        # self.headers = get_user_headers_by_login(self, self.email, self.password)
        self.headers = get_user_headers_by_account_id(self.account_id)

        self.payment_method = get_payment_method(self, self.headers)

        self.sku_read_code = random.choice(self.sku_read_codes)
        self.outlet= random.choice(self.outlets)
        self.sku_write = {
            "code": random.choice(self.sku_write_codes),
            "quantity": 1,
            "unitPrice": 300,
        }

    @task(6)
    def get_listing(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/listings/" + self.sku_read_code,
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(10)
    def get_related_listings(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/listings/" + self.sku_read_code + "/related",
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(12)
    def get_listing_locations(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/listings/" + self.sku_read_code + "/locations",
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(2)
    def get_listing_outlets(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/listings/outlets/" + self.outlet,
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(2)
    def get_vouchers(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/vouchers",
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(4)
    def get_orders(self) -> None:
        res = self.client.get(
            url="/ecommerce/mobile/orders",
            headers=self.headers,
        )
        # print(res.json())
        res.close()

    @task(2)
    def purchase_otp(self) -> None:
        ref_id = str(uuid4())
        purchase_data = {
            "refId": ref_id,
            "items": [
                {
                    "sku": self.sku_write["code"],
                    "quantity": self.sku_write["quantity"],
                    "unitPrice": self.sku_write["unitPrice"],
                }
            ],
            "paymentMethods": [
                {
                    "type": "cashback",
                    "amount": self.sku_write["quantity"] * self.sku_write["unitPrice"],
                }
            ],
            "total": self.sku_write["quantity"] * self.sku_write["unitPrice"],
        }

        with self.client.post(
            url="/ecommerce/mobile/orders",
            headers=self.headers,
            json=purchase_data,
            catch_response=True,
        ) as purchase_res:
            if purchase_res.status_code == 429:
                purchase_res.success()

            purchase_json = purchase_res.json()
            purchase_res.close()

            if (
                "data" not in purchase_json
                or "status" not in purchase_json["data"]
                or purchase_json["data"]["status"] != "pending-otp"
                or "orderNumber" not in purchase_json["data"]
                or "requestIdOtp" not in purchase_json["data"]
            ):
                raise RuntimeError(f"Unsuccessful response: {purchase_json}")

            resume_data = {
                "orderNumber": purchase_json["data"]["orderNumber"],
                "otp": "000000",
                "requestIdOtp": purchase_json["data"]["requestIdOtp"],
            }
            resume_res = self.client.post(
                url="/ecommerce/mobile/orders/resumeOtp",
                headers=self.headers,
                json=resume_data,
            )
            # print(resume_res.json())
            resume_res.close()


    @task(6)
    def purchase_non_3ds(self) -> None:
        ref_id = str(uuid4())
        data = {
            "refId": ref_id,
            "items": [
                {
                    "sku": self.sku_write["code"],
                    "quantity": self.sku_write["quantity"],
                    "unitPrice": self.sku_write["unitPrice"],
                }
            ],
            "paymentMethods": [
                {
                    "type": "card",
                    "amount": self.sku_write["quantity"] * self.sku_write["unitPrice"],
                    "paymentMethodAccountId": self.payment_method,
                }
            ],
            "total": self.sku_write["quantity"] * self.sku_write["unitPrice"],
        }

        with self.client.post(
            url="/ecommerce/mobile/orders",
            headers=self.headers,
            json=data,
            catch_response=True,
        ) as res_post:
            if res_post.status_code == 429:
                res_post.success()

            # print(res_post.json())
            res_post.close()


    @task(2)
    def purchase_split(self) -> None:
        ref_id = str(uuid4())
        data = {
            "refId": ref_id,
            "items": [
                {
                    "sku": self.sku_write["code"],
                    "quantity": self.sku_write["quantity"],
                    "unitPrice": self.sku_write["unitPrice"],
                }
            ],
            "paymentMethods": [
                {
                    "type": "cashback",
                    "amount": self.cashback_to_pay,
                },
                {
                    "type": "card",
                    "amount": self.sku_write["quantity"] * self.sku_write["unitPrice"] - self.cashback_to_pay,
                    "paymentMethodAccountId": self.payment_method,
                }
            ],
            "total": self.sku_write["quantity"] * self.sku_write["unitPrice"],
        }

        with self.client.post(
            url="/ecommerce/mobile/orders",
            headers=self.headers,
            json=data,
            catch_response=True,
        ) as res_post:
            if res_post.status_code == 429:
                res_post.success()

            # print(res_post.json())
            res_post.close()


class EcommerceUser(HttpUser):
    wait_time = between(3, 10)
    tasks = [UserBehaviour]
