# cmd to run locally: ./scripts/local_start.sh gateway.dev.shopback.com pos-integration/test_pos-integration tasksall
# rmb to add --platform linux/amd64 to local_start.sh when running locally
from locust import HttpUser, task, between, TaskSet
from datetime import datetime
from auth_utility import generate_hmac_signature
from uuid import uuid4

def get_headers(contentType: str, method: str, pathWithQuery: str, body: object, accessKeyId: str, accessKeySecret: str): 
    isoNow = datetime.utcnow().isoformat()
    isoNow = isoNow[:-4] + isoNow[-1] + "Z"
    params = {}
    params['body'] = body
    params['contentType'] = contentType
    params['timestamp'] = isoNow
    params['method'] = method
    params['pathWithQuery'] = pathWithQuery
    return {
        "date": isoNow,
        "authorization": "SB1-HMAC-SHA256 " + accessKeyId + ":" + generate_hmac_signature(params, accessKeySecret),
        "content-type": contentType,
    }

class CoreApis(TaskSet): 
    #load-test-integration-partner
    accessKeyId = "bab8-8dd588-a1c746"
    accessKeySecret = "b773216f36b65353ce61f23fef33caaca35ed59e6e8b9ae1"
    hasOrderCreated = False
    hasBeenValidated = False
    order_reference_id = "f6738b94-6eab-44b0-ba27-bfd9ba089dc8"

    @task(1)
    def create_instore_dynamic_order(self) -> None:
        contentType = 'application/json'
        method = 'POST'
        pathWithQuery= "http://gateway.dev.shopback.com/posi/v1/instore/order/create" # Update base URL if necessary
        self.order_reference_id =  str(uuid4())
        data = {
            "amount": 5050, # in cents
            "posId": "a1w850000000NavAAE", # has to be present and active in MIS 
            "country": "SG",
            "currency": "SGD",
            "referenceId":  self.order_reference_id,
            "qrType": "payload"
        }

        print("==== [External] Initiating Order...", self.order_reference_id)
        res = self.client.post(
            url="/posi/v1/instore/order/create",
            json=data,
            headers=get_headers(contentType, method, pathWithQuery, data, self.accessKeyId, self.accessKeySecret),
        )
        if res.ok: 
            self.hasOrderCreated = True
            self.hasBeenValidated = False
        else: 
            print("!!! Error for Initiate Order", res.json())
            self.hasOrderCreated = False

        res.close()
        
    # NOTE: This test will NOT work locally, please comment out when necessary.  
    @task(1)
    def validate_order(self) -> None:
        if self.hasOrderCreated == False: 
            print("exiting..... no order created yet")
            self.hasBeenValidated = False
            self.interrupt()

        if self.hasBeenValidated == True: 
            print("exiting..... order has already been validated")
            self.hasOrderCreated == False
            self.hasBeenValidated = False
            self.interrupt()

        print("==== [INTERNAL] Validating Order...", self.order_reference_id)
        res = self.client.patch(
            url="/posi/internal/v1/order/validate",
            json={
                "referenceId": self.order_reference_id,
                "terminalId": "a1w850000000NavAAE",
                "externalId": "pos-load-test-" + str(uuid4()),
                "orderAmount": 5050,
            }
        )
        print("==== [INTERNAL] Validating Order Res", res.json())
        if res.ok: 
            self.hasBeenValidated = True
        else: 
            print("!!! Error for Validate Order", res.json())

        res.close()

    @task(3)
    def get_order_details(self) -> None:
        if self.hasOrderCreated == False: 
            print("exiting..... no order created yet")
            self.hasBeenValidated = False
            self.interrupt()

        contentType = 'application/x-www-form-urlencoded'
        method = 'GET'
        pathWithQuery= "http://gateway.dev.shopback.com/posi/v1/instore/order/" + self.order_reference_id # Update base URL if necessary

        print("==== [External] Get Order Details...", self.order_reference_id)
        res = self.client.get(
            url="/posi/v1/instore/order/" + self.order_reference_id,
            headers=get_headers(contentType, method,pathWithQuery, {}, self.accessKeyId, self.accessKeySecret),
        )

        if not res.ok: 
            print("!!! Error for Get Order Details", res.json())

        res.close()

    @task(1)
    def stop(self):
        print("Exiting Task Set.....")
        self.hasOrderCreated = False
        self.hasBeenValidated = False
        self.interrupt()

class IntegrationPartner(HttpUser): 
    wait_time = between(3, 8)
    tasks = [CoreApis]

    
        