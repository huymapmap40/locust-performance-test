import json
import random

from account_ids import users_for_static_orders, users_with_some_orders
from locust import HttpUser, between, task
from users_utility import get_user_headers_by_account_id

static_payload_1 = 'https://app.hoolah.co/qr?scan=0002010102115303702263600324b8e136e356b4b67a37d223d7ca566de520434255802SG5920Hoolah%20Zen%20Singapore6009Singapore622405203231363246373433433863041452'

class User(HttpUser):
    wait_time = between(1, 3)
    account_id = 0
    headers = {}

    @task(10)
    def get_user_summary(self):
        self.account_id = random.choice(users_with_some_orders)
        self.headers = get_user_headers_by_account_id(self.account_id)
        self.headers['Cache-Control'] = 'no-cache'

        self.client.get(url="/sbpay/pay-later/v1/users/summary", headers=self.headers, name="Pay Later User Summary")

    @task(10)
    def get_user_outstanding_debt(self):
        self.account_id = random.choice(users_with_some_orders)
        self.headers = get_user_headers_by_account_id(self.account_id)
        self.headers['Cache-Control'] = 'no-cache'
        url = f'/sbpay/internal/pay-later/v1/users/{self.account_id}/outstanding-debt';
        print(url)
        self.client.get(url=f'/sbpay/internal/pay-later/v1/users/{self.account_id}/outstanding-debt', headers=self.headers, name="Pay Later User Outstanding Debt")

    @task(1)
    def scan_qr(self):
        self.account_id = random.choice(users_with_some_orders)
        self.headers = get_user_headers_by_account_id(self.account_id)
        self.headers['Cache-Control'] = 'no-cache'

        data = {
          "payload": static_payload_1,
        }
        self.client.post(url="/sbpay/pay-later/v1/qr/scan", headers=self.headers, json=data, name="Pay Later Scan QR")
    
    @task(1)
    def get_payment_methods(self):
        self.account_id = random.choice(users_with_some_orders)
        self.headers = get_user_headers_by_account_id(self.account_id)
        self.headers['Cache-Control'] = 'no-cache'

        self.client.get(url="/sbpay/pay-later/v1/payment-methods", headers=self.headers, name="Pay Later Payment Methods")
    
    @task(1)
    def create_and_confirm_static_order_without_promo(self):
        self.account_id = random.choice(users_for_static_orders)
        self.headers = get_user_headers_by_account_id(self.account_id)
        self.headers['Cache-Control'] = 'no-cache'

        data = {
          "payload": static_payload_1,
          "amount": 600,
        }
        res = self.client.post(url="/sbpay/pay-later/v1/orders", headers=self.headers, json=data, name="Create Static Order")

        if res.status_code == 201 :
          data = json.loads(res.text)
          pay_url = f'/sbpay/pay-later/v1/orders/{data["data"]["id"]}/confirm'
          first_installment_amount = data['data']['installmentSummary'][0]['amount']

          # Make sure the test user has default payment method
          # use default card for payment
          payment_method = next((item for item in data['data']['paymentMethods'] if item["isDefault"] == True), None)
          payment_method_account_id = payment_method['_id']

          pay_headers = self.headers.copy()
          pay_headers['x-shopback-client-user-agent'] = 'tbd'
          pay_headers['x-device-id'] = 'tbd'
          pay_headers['x-shopback-device-model'] = 'tbd'

          pay_body = {
              "amount": first_installment_amount,
              "paymentMethods": [{
                  "amount": first_installment_amount,
                  "category": "card",
                  "type": "card",
                  "paymentMethodAccountId": payment_method_account_id
              }]
          }

          res = self.client.post(url=pay_url, headers=pay_headers, json=pay_body, name="Confirm Static Order")
