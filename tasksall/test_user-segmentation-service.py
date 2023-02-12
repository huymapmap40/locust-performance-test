import json
import base64
import random

from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    def craftLoadTestToRetentionSegment(self):
        randomAccountId = random.randint(10000, 5000000)
        queries = [
            {
                "key": "sboc:retention-new-customer-rolling-30-day"
            },
            {
                "key": "sboc:retention-current-customer-rolling-30-day"
            },
            {
                "key": "sboc:retention-lapsed-customer-rolling-30-day"
            },
            {
                "key": "sboc:retention-churned-customer-rolling-30-day"
            },
            {
                "key": "sboc:retention-resurrect-customer-rolling-30-day"
            }
        ]
        return {
            "includeOutput": True,
            "requester": "locust",
            "accountId": randomAccountId,
            "queries": queries
        }

    def craftLightBulkClassifyBody(self): 
        randomAccountId = random.randint(10000, 5000000)
        queries = [
            {
                "key": "sboc:is-new-customer"
            },
            {
                "key": "sb:has-verified-phone-number"
            },
            {
                "params": {
                    "start": "2021-06-01 00:00:00",
                    "end": "2021-06-05 00:00:00",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ]
                },
                "key": "sbgo:unique-brands-count-within-date-range-above-threshold"
            },
            {
                "params": {
                    "start": "2021-05-05 18:15:19",
                    "end": "2021-05-10 18:15:19",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:unique-merchants-count-within-date-range-above-threshold-v3"
            },
            {
                "params": {
                    "start": "2019-05-01 18:15:10019",
                    "end": "2021-05-05 18:15:19",
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:made-order-within-date-range-v3"
            },
        ]
        
        return {
            "includeOutput": True,
            "accountId": randomAccountId,
            "queries": queries,
            "requester": "locust"
        }

    def craftMediumBulkClassifyQuery(self):
        randomAccountId = random.randint(10000, 5000000)
        queries = [
            {
                "key": "sboc:is-new-customer"
            },
            {
                "params": {
                    "start": "2015-05-01 18:15:19",
                    "end": "2021-05-10 18:15:19"
                },
                "key": "signup-within-date-range"
            },
            {
                "params": {
                    "start": "2019-05-01 18:15:10019",
                    "end": "2021-05-05 18:15:19",
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:made-order-within-date-range-v3"
            },
            {
                "params": {
                    "start": "2019-06-01 00:00:00",
                    "end": "2021-06-05 00:00:00",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ]
                },
                "key": "sbgo:unique-brands-count-within-date-range-above-threshold"
            },
            {
                "params": {
                    "start": "2019-05-05 18:15:19",
                    "end": "2021-05-10 18:15:19",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:unique-merchants-count-within-date-range-above-threshold-v3"
            },
        ]
        
        return {
            "includeOutput": True,
            "accountId": randomAccountId,
            "queries": queries,
            "requester": "locust"
        }
    
    def craftLargeBulkClassifyQuery(self):
        randomAccountId = random.randint(10000, 5000000)
        queries = [
            {
                "key": "sb:has-verified-cashout-method"
            },
            {
                "params": {
                    "start": "2012-01-01 00:00:00",
                    "end": "2015-06-01 00:00:00",
                    "thresholdFriends": 1
                },
                "key": "raf:referred-min-within-date-range"
            },
            {
                "params": {
                    "start": "2017-05-01 18:15:10019",
                    "end": "2021-05-05 18:15:19",
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:made-order-within-date-range-v3"
            },
            {
                "params": {
                    "start": "2017-06-01 00:00:00",
                    "end": "2021-06-05 00:00:00",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ]
                },
                "key": "sbgo:unique-brands-count-within-date-range-above-threshold"
            },
            {
                "params": {
                    "start": "2017-05-05 18:15:19",
                    "end": "2021-05-10 18:15:19",
                    "threshold": 1,
                    "cashbackStatus": [
                        "Pending",
                        "Redeemable",
                        "Paid"
                    ],
                    "excludeEoutletIds": [],
                    "platforms": [
                        "web",
                        "android",
                        "extension"
                    ]
                },
                "key": "sboc:unique-merchants-count-within-date-range-above-threshold-v3"
            },
        ]
        
        return {
            "includeOutput": True,
            "accountId": randomAccountId,
            "queries": queries,
            "requester": "locust"
        }
    
    @task(5)
    def testLightBulkClassify(self):
        r = self.client.post(
            url="/queries/bulk-classify",
            data=json.dumps(self.craftLightBulkClassifyBody()),
            headers={"Content-Type": "application/json"}
        )

    @task(3)
    def testMediumBulkClassify(self):
        r = self.client.post(
            url="/queries/bulk-classify",
            data=json.dumps(self.craftMediumBulkClassifyQuery()),
            headers={"Content-Type": "application/json"}
        )

    @task(1)
    def testHeavyBulkClassify(self):
        r = self.client.post(
            url="/queries/bulk-classify",
            data=json.dumps(self.craftLargeBulkClassifyQuery()),
            headers={"Content-Type": "application/json"}
        )
    
    @task(3)
    def testRetention(self):
        r = self.client.post(
            url="/queries/bulk-classify",
            data=json.dumps(self.craftLoadTestToRetentionSegment()),
            headers={"Content-Type": "application/json"}
        )

class WebsitUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
