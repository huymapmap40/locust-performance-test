import urllib
from locust import HttpUser, TaskSet, task
from random import randint
import datetime

class UserBehavior(TaskSet):
    @task
    def upsertCashback(self):
        """Upsert cashbacks"""
        self.client.post(
            "/upsert/cashback",
            json={
                "cashbackType": "affiliate",
                "accountId": 12345,
                "entity": "sboc",
                "groupId": None,
                "amount": 123.0,
                "title": "title",
                "description": "description",
                "status": "Pending",
                "transactionDatetimeUtc": "2022-01-16T00:00:00.000Z",
                "availableByDatetimeUtc": "2022-01-16T00:00:00.000Z",
                "clientUpdatedDatetimeUtc": datetime.datetime.now().isoformat(),
                "context": {
                    "commission": {
                        "purchaseAmount": 123.0,
                        "commissionAmount": 0,
                        "commissionablePurchaseAmount": 0
                    },
                    "reference": {
                        "source": "load-testing",
                        "sourceId": str(randint(0, 1000))
                    },
                    "template": {
                        "name": "default",
                        "value": {
                            "userStatusTypeKey": "CB_PENDING_NORMAL",
                            "isTravel": False
                        }
                    },
                    "reporting": {
                        "affiliate": {
                            "test": "test value 1"
                        },
                        "affiliateExtended": {
                            "data": [
                                "array element 1",
                                "array element 2"
                            ]
                        }
                    }
                }
            },
            headers={'content-type': 'application/json'}
        )
    
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 100
    max_wait = 1000