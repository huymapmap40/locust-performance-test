from pymongo import MongoClient, ASCENDING, DESCENDING, ReturnDocument
from bson.objectid import ObjectId
import random
from datetime import datetime
from uuid import uuid4
from locust import TaskSet, User, task, between
from utility_users import get_unique_account_id

STAGING_SG_ECOMM_MONGO_URI = ""
STAGING_SG_SBOC_MONGO_URI = ""

if not STAGING_SG_ECOMM_MONGO_URI or not STAGING_SG_SBOC_MONGO_URI:
    raise AssertionError(
        "Please specify STAGING_SG_ECOMM_MONGO_URI and STAGING_SG_SBOC_MONGO_URI"
    )

ecomm_mongo_client = MongoClient(STAGING_SG_ECOMM_MONGO_URI)
sboc_mongo_client = MongoClient(STAGING_SG_SBOC_MONGO_URI)

db_ecomm = ecomm_mongo_client.ecommerce
db_plo = sboc_mongo_client.paymentlinkedoffers
db_ars = ecomm_mongo_client["app-reward"]

# db_ecomm
col_inventories = db_ecomm.inventories
col_user_inventories = db_ecomm.userinventories
col_payment_methods_ecomm = db_ecomm.paymentmethods
col_commercials = db_ecomm.commercials
col_ops_configs_ecomm = db_ecomm.opsconfigs
col_orders = db_ecomm.orders
col_payment_provider_transactions = db_ecomm.paymentprovidertransactions

# db_plo
col_user_profiles = db_plo["user-profiles"]
col_mobile_configurations = db_plo["mobile-configurations"]
col_sets = db_plo.sets
col_cashback_rates = db_plo["cashback-rates"]
col_outlets = db_plo.outlets
col_transactions = db_plo.transactions
col_appsflyer = db_plo.appsflyer
col_activations = db_plo.activations2
col_payment_methods_plo = db_plo.paymentmethods
col_user_actions = db_plo["user-actions"]
col_partner_deals = db_plo["partner-deals"]
col_ops_configs_plo = db_plo.opsconfig

# db_ars
col_vouchers = db_ars.vouchers

read_accounts = [
    3779069,
    2302229,
    5063301,
    177887,
    4992167,
    4427549,
    3708851,
    5050117,
    4956850,
    5060467,
]

read_skus = [
    {"_id": ObjectId("5f6c77eb09273804e108410f"), "code": "SBGOECOMMCVINNI1"},
    {"_id": ObjectId("5efb0da3eb99a30419cb6402"), "code": "SBGOECOMMSVBFSF4"},
    {"_id": ObjectId("5f9bcb1194bef406a15e2904"), "code": "SBGOECOMMSVGC13"},
    {"_id": ObjectId("5f5369f48e400e232dec2055"), "code": "SBGOECOMMCVKFOOD1"},
    {"_id": ObjectId("5f2b691de427335ea7a6801b"), "code": "SBGOECOMMSVBFSF6"},
    {"_id": ObjectId("5f7a46755a010a7b8e6820df"), "code": "SBGOECOMMSVHEYYO3"},
    {"_id": ObjectId("5f3d04fadd49c720f460d0b7"), "code": "SBGOECOMMCVGTWO1"},
    {"_id": ObjectId("5f743506b53cba05e4998dac"), "code": "SBGOECOMMSVPHST2"},
    {
        "_id": ObjectId("5f081aaabb71fa14c005659e"),
        "code": "SBGOECOMMCVPAG2",
    },
    {"_id": ObjectId("5f2b691de427332cbea68021"), "code": "SBGOECOMMSVCTF4"},
]

write_skus = [
    {"_id": ObjectId("5fbcc7f732fdb33f73cbc7e5"), "code": "LOAD_TESTER_0"},
    {"_id": ObjectId("5fbcc7f732fdb334fbcbc7eb"), "code": "LOAD_TESTER_1"},
    {"_id": ObjectId("5fbcc7f732fdb31f10cbc7f1"), "code": "LOAD_TESTER_2"},
    # {"_id": ObjectId("5fbcc7f832fdb34d72cbc7f7"), "code": "LOAD_TESTER_3"},
    # {"_id": ObjectId("5fbcc7f832fdb33c50cbc7fd"), "code": "LOAD_TESTER_4"},
    # {"_id": ObjectId("5fbcc7f932fdb36478cbc803"), "code": "LOAD_TESTER_5"},
    # {"_id": ObjectId("5fbcc7f932fdb345bfcbc809"), "code": "LOAD_TESTER_6"},
    # {"_id": ObjectId("5fbcc7f932fdb37e49cbc80f"), "code": "LOAD_TESTER_7"},
    # {"_id": ObjectId("5fbcc7fa32fdb3c66ecbc815"), "code": "LOAD_TESTER_8"},
    # {"_id": ObjectId("5fbcc7fa32fdb3645bcbc81b"), "code": "LOAD_TESTER_9"},
]

cashback_rates = [
    ObjectId("5fb278f33902f4b2c9a75e70"),
    ObjectId("5fb278f33902f45232a75e6f"),
    ObjectId("5fb22d8ffc2f5be21c317c1c"),
    ObjectId("5fb22d8ffc2f5bc62f317c1e"),
    ObjectId("5fb22d8ffc2f5b7272317c1a"),
    ObjectId("5fb22d8ffc2f5b6c8d317c1d"),
    ObjectId("5fb22d8ffc2f5b0ad3317c1b"),
    ObjectId("5faad3f6a2c761e460f6dd16"),
    ObjectId("5fa93beda2c761f832f6dd0f"),
    ObjectId("5fa93beda2c761e547f6dd0d"),
    ObjectId("5fa93beda2c761e405f6dd13"),
    ObjectId("5fa93beda2c761df4cf6dd0c"),
    ObjectId("5fa93beda2c761daa3f6dd0e"),
    ObjectId("5fa93beda2c761a367f6dd14"),
    ObjectId("5fa93beda2c76199aff6dd0b"),
    ObjectId("5fa93beda2c7618565f6dd15"),
    ObjectId("5fa93beda2c7616a6df6dd10"),
    ObjectId("5fa93beda2c76137daf6dd11"),
    ObjectId("5fa93beda2c761237ef6dd12"),
    ObjectId("5fa93beda2c761222df6dd0a"),
    ObjectId("5f9cf17c62e80f0fc80a1427"),
    ObjectId("5f7358c94e34840f62d1816d"),
    ObjectId("5f7358c94e34840f62d1816d"),
    ObjectId("5f7358c94e34840f62d1816d"),
    ObjectId("5f7358c94e34840f62d1816d"),
]

outlets = [
    "0014296",
    "0014295",
    "0014294",
    "0014293",
    "0014292",
    "0014284",
    "0014283",
    "0014280",
    "0014279",
    "0014277",
    "0000301",
    "0001067",
    "0001398",
    "0001398",
    "0002070",
    "0002449",
    "0002727",
    "0003484",
    "0003484",
    "0003484",
    "0004873",
    "0013166",
    "0004041",
    "0013159",
    "0010772",
    "0013154",
    "0013157",
    "0010916",
    "0012309",
    "0010917",
    "0009891",
    "0009905",
    "0011184",
    "0007758",
]

brands = [
    "0003121",
    "0000397",
    "0009756",
    "0011268",
    "0009135",
    "0002329",
    "0003818",
    "0006631",
    "0009489",
    "0003877",
    "0001433",
    "0021101",
    "0010234",
    "0000244",
    "0020580",
    "0000793",
    "0002264",
    "0006670",
    "0011497",
    "0020585",
    "0000790",
    "0001651",
]


class EcommBehaviour(TaskSet):
    read_account_id = 0
    write_account_id = 0
    payment_method = ""

    def on_start(self) -> None:
        self.read_account_id = random.choice(read_accounts)
        self.write_account_id = get_unique_account_id()
        self.payment_method = f"LOAD_TESTER_{self.write_account_id}"

    @task(4520)
    def get_inventory(self) -> None:
        codes = list(map(lambda sku: sku["code"], read_skus))
        codes.extend(list(map(lambda sku: sku["code"], write_skus)))

        query_inventories = {
            "bu": "sbgo",
            "code": {"$in": codes},
            "isPublic": True,
            "isDeleted": False,
        }
        cursor_inventories = col_inventories.find(query_inventories)
        # for doc in cursor_inventories:
        #     print(doc)

        inventory = list(map(lambda sku: sku["_id"], read_skus))
        inventory.extend(list(map(lambda sku: sku["_id"], write_skus)))

        query_userinventories = {
            "accountId": self.read_account_id,
            "inventory": {"$in": inventory},
            "currentStatus": {
                "$in": [
                    "purchased",
                    "pending",
                    "used",
                    "expired",
                    "voided",
                    "comingSoon",
                    "reserved",
                ]
            },
        }
        cursor_user_inventories = col_user_inventories.find(query_userinventories)
        # for doc in cursor_user_inventories:
        #     print(doc)

    @task(1083)
    def get_sku_locations(self) -> None:
        read_sku = random.choice(read_skus)

        query_inventories = {
            "code": read_sku["code"],
            "isDeleted": False,
        }
        sku = col_inventories.find_one(query_inventories)
        # print(sku)

        query_commercials = {"sku": {"$in": [read_sku["code"]]}}
        cursor_commercials = col_commercials.find(query_commercials)
        # for doc in cursor_commercials:
        #     print(doc)

    @task(996)
    def get_sku_detail(self) -> None:
        query_payment_methods = {"accountId": self.read_account_id}
        cursor_payment_methods = col_payment_methods_ecomm.find(
            query_payment_methods
        ).sort("history.0.occurredAt", DESCENDING)
        # for doc in cursor_payment_methods:
        #     print(doc)

        read_sku = random.choice(read_skus)

        query_inventories = {
            "bu": "sbgo",
            "code": read_sku["code"],
            "isPublic": True,
            "isDeleted": False,
        }
        sku = col_inventories.find_one(query_inventories)
        # print(sku)

        query_commercials = {"sku": {"$in": [read_sku["code"]]}}
        cursor_commercials = col_commercials.find(query_commercials)
        # for doc in cursor_commercials:
        #     print(doc)

        query_userinventories = {
            "accountId": self.read_account_id,
            "inventory": read_sku["_id"],
            "currentStatus": {
                "$in": [
                    "purchased",
                    "pending",
                    "used",
                    "expired",
                    "voided",
                    "comingSoon",
                    "reserved",
                ]
            },
        }
        cursor_user_inventories = col_user_inventories.find(query_userinventories)
        # for doc in cursor_user_inventories:
        #     print(doc)

    @task(732)
    def get_related_skus(self) -> None:
        read_sku = random.choice(read_skus)

        query_one_inventories = {
            "code": read_sku["code"],
            "isDeleted": False,
        }
        sku = col_inventories.find_one(query_one_inventories)
        # print(sku)

        query_one_commercials = {"sku": {"$in": [read_sku["code"]]}}
        cursor_one_commercials = col_commercials.find(query_one_commercials)
        # for doc in cursor_one_commercials:
        #     print(doc)

        now = datetime.now()

        query_two_inventories = {
            "scopeIds": sku["scopeIds"] if len(sku["scopeIds"]) == 1 else { "$size": len(sku["scopeIds"]), "$all": sku["scopeIds"] },
            "scope": sku["scope"],
            "isPublic": True,
            "startsOn": {
                "$lte": now,
            },
            "endsOn": {
                "$gt": now,
            },
            "stockLevel.available": {"$gt": 0},
            "code": {"$ne": sku["code"]},
            "isDeleted": False,
        }
        cursor_inventories = col_inventories.find(query_two_inventories)
        for doc in cursor_inventories:
            # print(doc)

            query_two_commercials = {"sku": {"$in": [doc["code"]]}}
            cursor_two_commercials = col_commercials.find(query_two_commercials)
            # for doc in cursor_two_commercials:
            #     print(doc)

    @task(109)
    def create_order_credit_card(self) -> None:
        if self.write_account_id == 0:
            return

        query_one_ops_configs = {"key": "rate-limit-local-max-in-progress-request"}
        rate_limit_local = col_ops_configs_ecomm.find_one(query_one_ops_configs)
        # print(rate_limit_local)

        query_two_ops_configs = {"key": "rate-limit-global-max-in-progress-request"}
        rate_limit_global = col_ops_configs_ecomm.find_one(query_two_ops_configs)
        # print(rate_limit_global)

        query_one_payment_methods = {
            "paymentMethodAccountId": {"$in": [self.payment_method]}
        }
        cursor_payment_methods = col_payment_methods_ecomm.find(
            query_one_payment_methods
        )
        # for doc in cursor_payment_methods:
        #   print(doc)

        payment_method = list(cursor_payment_methods)[0]
        # print(payment_method)

        write_sku = random.choice(write_skus)

        query_inventories = {"code": write_sku["code"], "isDeleted": False}
        query_commercials = {"sku": {"$in": [write_sku["code"]]}}

        for i in range(2):
            sku = col_inventories.find_one(query_inventories)
            # print(sku)

            cursor_commercials = col_commercials.find(query_commercials)
            # for doc in cursor_commercials:
            #     print(doc)

        now = datetime.now()

        order_number = uuid4().hex
        order_req = {
            "accountId": self.write_account_id,
            "refId": str(uuid4()).upper(),
            "orderNumber": order_number,
            "publisherReference": uuid4().hex,
            "deviceId": str(uuid4()).upper(),
            "subtotal": 1,
            "total": 1,
            "items": [
                {
                    "refIds": [
                        f"{order_number}-0",
                    ],
                    "_id": write_sku["_id"],
                    "sku": write_sku["code"],
                    "quantity": 1,
                    "unitPrice": 1,
                }
            ],
            "paymentMethods": [
                {
                    "_id": payment_method["_id"],
                    "paymentMethodAccountId": self.payment_method,
                    "type": "card",
                },
            ],
            "lifecycle": [
                {
                    "_id": ObjectId(),
                    "status": "init",
                    "datetime": now,
                }
            ],
            "surcharges": [],
            "paymentReceipts": [],
            "createdAt": now,
            "updatedAt": now,
            "__v": 0,
        }
        order = col_orders.insert_one(order_req)
        # print(order.inserted_id)

        sku = col_inventories.find_one(query_inventories)
        # print(sku)

        cursor_commercials = col_commercials.find(query_commercials)
        # for doc in cursor_commercials:
        #     print(doc)

        query_userinventories = {
            "accountId": self.write_account_id,
            "inventory": {"$in": [write_sku["_id"]]},
            "currentStatus": {
                "$in": [
                    "purchased",
                    "pending",
                    "used",
                    "expired",
                    "voided",
                    "comingSoon",
                    "reserved",
                ]
            },
        }
        cursor_user_inventories = col_user_inventories.find(query_userinventories)
        # for doc in cursor_user_inventories:
        #     print(doc)

        now = datetime.now()

        filter_one_inventories = {
            "code": write_sku["code"],
            "stockLevel.available": {"$gte": 1},
            "endsOn": {"$gt": now},
            "isDeleted": False,
        }
        update_one_inventories = {
            "$inc": {"stockLevel.available": -1, "stockLevel.reserved": 1}
        }
        update_one_result = col_inventories.update_one(
            filter_one_inventories, update_one_inventories
        )
        # print(update_one_result.modified_count)

        now = datetime.now()

        user_inventory_req = {
            "accountId": self.write_account_id,
            "inventory": sku["_id"],
            "orderRef": f"{order_number}-0",
            "bu": sku["bu"],
            "scope": sku["scope"],
            "scopeIds": sku["scopeIds"],
            "currentStatus": "reserved",
            "currentStatusIndex": 7,
            "reservedAt": now,
            "usedAt": None,
            "expiredAt": None,
            "freedAt": None,
            "voidedAt": None,
            "voidedBy": None,
            "endsOn": sku["validityEndDate"],
            "createdAt": now,
            "updatedAt": now,
            "__v": 0,
            "voucherId": None,
            "voucherRedirectLink": None,
        }
        inserted = col_user_inventories.insert_many([user_inventory_req])
        # for i in inserted.inserted_ids:
        # print(i)

        order_filter = {
            "_id": order.inserted_id,
            "lifecycle.0.status": {"$in": ["init"]},
        }
        order_update = {
            "$push": {
                "lifecycle": {
                    "$each": [
                        {
                            "_id": ObjectId(),
                            "status": "reserved",
                            "datetime": datetime.now(),
                        }
                    ],
                    "$position": 0,
                }
            }
        }
        updated = col_orders.find_one_and_update(
            order_filter, order_update, return_document=ReturnDocument.AFTER
        )
        # print(updated)

        for i in range(2):
            query_two_payment_methods = {
                "paymentMethodAccountId": self.payment_method,
            }
            payment_method = col_payment_methods_ecomm.find_one(
                query_two_payment_methods
            )
            # print(payment_method)

        now = datetime.now()
        txn_filter = {"orderNumber": order_number, "transactionType": "purchase"}
        txn_update = {
            "$set": {
                "accountId": self.write_account_id,
                "orderNumber": order_number,
                "paymentMethodAccountId": self.payment_method,
                "requestId": f"{uuid4().hex}-purchase",
                "transactionId": uuid4().hex,
                "transactionType": "purchase",
                "transactionAmount": 1,
                "provider": "checkout-vgs",
                "createdAt": now,
                "updatedAt": now,
                "remarks": ["10000"],
                "status": "success",
            }
        }
        txn = col_payment_provider_transactions.find_one_and_update(
            txn_filter, txn_update, upsert=True, return_document=ReturnDocument.AFTER
        )
        # print(txn)

        order_filter = {
            "_id": order.inserted_id,
            "lifecycle.0.status": {"$in": ["reserved", "auth-received"]},
        }
        order_update = {
            "$push": {
                "lifecycle": {
                    "$each": [
                        {
                            "_id": ObjectId(),
                            "status": "paid",
                            "datetime": datetime.now(),
                        }
                    ],
                    "$position": 0,
                }
            }
        }
        updated = col_orders.find_one_and_update(
            order_filter, order_update, return_document=ReturnDocument.AFTER
        )
        # print(updated)

        query_user_inventories = {
            "accountId": self.write_account_id,
            "orderRef": {"$in": [f"{order_number}-0"]},
            "currentStatus": {"$in": ["reserved", "pending"]},
            "voucherId": None,
        }
        cursor_user_inventories = col_user_inventories.find(query_user_inventories)
        # for doc in cursor_user_inventories:
        #     print(doc)

        query_inventories = {"_id": write_sku["_id"], "isDeleted": False}
        sku = col_inventories.find_one(query_inventories)
        # print(sku)

        query_userinventories = {
            "accountId": self.write_account_id,
            "inventory": {"$in": [write_sku["_id"]]},
            "currentStatus": {
                "$in": [
                    "purchased",
                    "pending",
                    "used",
                    "expired",
                    "voided",
                    "comingSoon",
                    "reserved",
                ]
            },
        }
        cursor_user_inventories = col_user_inventories.find(query_userinventories)
        # for doc in cursor_user_inventories:
        #     print(doc)

        filter_vouchers = {
            "campaignCode": write_sku["code"],
        }
        update_vouchers = {
            "$set": {
                "status": "linked",
            }
        }
        voucher = col_vouchers.find_one_and_update(
            filter_vouchers, update_vouchers, return_document=ReturnDocument.AFTER
        )
        # print(voucher)

        filter_user_inventories = {
            "orderRef": {"$in": [f"{order_number}-0"]},
            "accountId": self.write_account_id,
            "currentStatus": "reserved",
            "voucherId": None,
        }
        update_user_inventories = {
            "$set": {
                "currentStatus": "purchased",
                "currentStatusIndex": 0,
                "purchasedAt": datetime.now(),
                "voucherId": str(voucher["_id"]),
                "voucherRedirectLink": None,
                "updatedAt": datetime.now(),
            }
        }
        updated = col_user_inventories.update_many(
            filter_user_inventories, update_user_inventories
        )
        # print(updated.modified_count)

        filter_inventories = {
            "_id": write_sku["_id"],
            "stockLevel.reserved": {"$gte": 1},
            "isDeleted": False,
        }
        update_inventories = {
            "$inc": {
                "stockLevel.purchased": 1,
                "stockLevel.reserved": -1,
            },
            "$set": {
                "updatedAt": datetime.now(),
            },
        }
        updated = col_inventories.update_one(filter_inventories, update_inventories)
        # print(updated.modified_count)

    @task(88)
    def get_users_skus(self) -> None:
        query_userinventories = {
            "accountId": self.read_account_id,
            "currentStatus": {
                "$in": [
                    "purchased",
                    "pending",
                    "used",
                    "expired",
                    "voided",
                    "comingSoon",
                ]
            },
        }
        cursor_user_inventories = (
            col_user_inventories.find(query_userinventories)
            .sort(
                [
                    ("currentStatusIndex", ASCENDING),
                    ("freedAt", DESCENDING),
                    ("usedAt", DESCENDING),
                    ("endsOn", ASCENDING),
                ]
            )
            .limit(20)
        )
        for doc in cursor_user_inventories:
            # print(doc)
            query_inventories = {"_id": doc["inventory"]}
            sku = col_inventories.find_one(query_inventories)
            # print(sku)

            query_commercials = {"sku": {"$in": [sku["code"]]}}
            cursor_commercials = col_commercials.find(query_commercials)
            # for doc in cursor_commercials:
            #     print(doc)

    @task(2260)
    def stop(self) -> None:
        self.interrupt()


class PloBehaviour(TaskSet):
    read_account_id = 0

    def on_start(self) -> None:
        self.read_account_id = random.choice(read_accounts)

    @task(2931)
    def get_mobile_configurations(self) -> None:
        query_user_profiles = {"_id": self.read_account_id}
        user_profile = col_user_profiles.find_one(query_user_profiles)
        # print(user_profile)

        # hereafter cached in fact
        query_mobile_configurations = {"type": "screen", "isDeleted": {"$ne": True}}
        cursor_mobile_configurations = col_mobile_configurations.find(
            query_mobile_configurations
        ).sort(
            [
                ("priority", ASCENDING),
                ("createdAt", ASCENDING),
            ]
        )
        # for doc in cursor_mobile_configurations:
        #     print(doc)

        query_mobile_configurations = {"type": "config", "isDeleted": {"$ne": True}}
        cursor_mobile_configurations = col_mobile_configurations.find(
            query_mobile_configurations
        ).sort(
            [
                ("priority", ASCENDING),
                ("createdAt", ASCENDING),
            ]
        )
        # for doc in cursor_mobile_configurations:
        #     print(doc)

        query_mobile_configurations = {"_id": ObjectId("5f95a112f092f7f8b5a0fadc")}
        mobile_config = col_mobile_configurations.find_one(query_mobile_configurations)
        # print(mobile_config)

    @task(2036)
    def search_deals(self) -> None:
        query_sets = {"key": "sbgo-deal-group-all"}
        one_set = col_sets.find_one(query_sets)
        # print(one_set)

        query_cashback_rates = {
            "_id": {
                "$in": cashback_rates,
            },
            "type": {"$in": ["One Time Bonus"]},
        }
        cursor_cashback_rates = col_cashback_rates.find(query_cashback_rates)
        # for doc in cursor_cashback_rates:
        #     print(doc)

        query_outlets = {
            "$or": [{"_id": {"$in": outlets}}, {"brandId": {"$in": brands}}]
        }
        cursor_outlets = col_outlets.find(query_outlets)
        # for doc in cursor_outlets:
        #     print(doc)

        query_transactions = {
            "accountId": self.read_account_id,
            "cashbacks": {
                "$elemMatch": {
                    "rateId": {"$in": cashback_rates},
                    "status": {"$in": ["pending", "confirmed"]},
                }
            },
        }
        cursor_transactions = col_transactions.find(query_transactions)
        # for doc in cursor_transactions:
        #     print(doc)

        query_user_profiles = {"_id": self.read_account_id}
        user_profile = col_user_profiles.find_one(query_user_profiles)
        # print(user_profile)

    @task(1207)
    def get_payment_methods(self) -> None:
        query_payment_methods = {"accountId": self.read_account_id}
        cursor_payment_methods = col_payment_methods_plo.find(query_payment_methods)
        # for doc in cursor_payment_methods:
        #     print(doc)

    @task(698)
    def get_loyalty_badge(self) -> None:
        query_user_actions = {
            "type": "viewed-loyalty-list",
            "accountId": self.read_account_id,
        }
        cursor_user_actions = (
            col_user_actions.find(query_user_actions)
            .sort("occurredAt", DESCENDING)
            .limit(1)
        )
        # for doc in cursor_user_actions:
        #     print(doc)

    @task(616)
    def get_mobile_configuration(self) -> None:
        query_user_profiles = {"_id": self.read_account_id}
        user_profile = col_user_profiles.find_one(query_user_profiles)
        # print(user_profile)

        # hereafter cached in fact
        for i in range(2):
            query_mobile_configurations = {"_id": ObjectId("5f95a112f092f7f8b5a0fadc")}
            mobile_config = col_mobile_configurations.find_one(
                query_mobile_configurations
            )
            # print(mobile_config)

    @task(531)
    def add_appsflyer_data(self) -> None:
        query_appsflyer = {"accountId": self.read_account_id}
        cursor_appsflyer = col_appsflyer.find(query_appsflyer).sort("_id", DESCENDING)
        # for doc in cursor_appsflyer:
        #     print(doc)

        now = datetime.now()
        appsflyer_req = {
            "appsflyerId": "1591872249051-9653646",
            "platformTrackingId": "BAA025F1-399F-4F73-A528-44C8C5905CC3",
            "userAgent": "ios",
            "accountId": self.read_account_id,
            "isSyncedWithConversionService": False,
            "createdAt": now,
            "updatedAt": now,
        }
        appsflyer = col_appsflyer.insert_one(appsflyer_req)
        # print(appsflyer.inserted_id)

        appsflyer_filter = {"_id": ObjectId("5fbe2fe105fd632ac25b7305")}
        appsflyer_update = {
            "$set": {"isSyncedWithConversionService": True, "updatedAt": datetime.now()}
        }
        updated = col_appsflyer.find_one_and_update(
            appsflyer_filter, appsflyer_update, return_document=ReturnDocument.AFTER
        )
        # print(updated)

    @task(414)
    def filter_outlets_ecommerce(self) -> None:
        pass

    @task(409)
    def filter_outlets_mobile(self) -> None:
        query_user_profiles = {"_id": self.read_account_id}
        user_profile = col_user_profiles.find_one(query_user_profiles)
        # print(user_profile)

        now = datetime.now()
        query_cashback_rates = {
            "type": {"$in": ["Return", "One Time Bonus", "First Try Bonus"]},
            "startAt": {"$lte": now},
            "$and": [
                {"$or": [{"endAt": None}, {"endAt": {"$gt": now}}]},
                {
                    "$or": [
                        {"scope": "outlet", "scopeIds": {"$in": outlets}},
                        {"scope": "brand", "scopeIds": {"$in": brands}},
                    ]
                },
            ],
        }
        cursor_cashback_rates = col_cashback_rates.find(query_cashback_rates)
        # for doc in cursor_cashback_rates:
        #     print(doc)

        query_activations = {
            "accountId": self.read_account_id,
            "startAt": {
                "$lte": now,
            },
            "endAt": {
                "$gt": now,
            },
            "$or": [
                {"scope": "outlet", "scopeIds": {"$in": outlets}},
                {"scope": "brand", "scopeIds": {"$in": brands}},
            ],
        }
        cursor_activations = col_activations.find(query_activations)
        # for doc in cursor_activations:
        #     print(doc)

        query_transactions = {
            "accountId": self.read_account_id,
            "cashbacks": {
                "$elemMatch": {
                    "rateId": {"$in": cashback_rates},
                    "status": {"$in": ["pending", "confirmed"]},
                }
            },
        }
        cursor_transactions = col_transactions.find(query_transactions)
        # for doc in cursor_transactions:
        #     print(doc)

        query_partner_deals = {
            "$or": [
                {"scope": "outlet", "scopeIds": {"$in": outlets}},
                {"scope": "brand", "scopeIds": {"$in": brands}},
            ],
            "startsOn": {
                "$lte": now,
            },
            "endsOn": {
                "$gt": now,
            },
            "type": "creditCard",
            "isPublic": True,
            "eligibilityRules.binRange": {
                "$in": [
                    "493725",
                    "456598",
                    "526471",
                    "462845",
                    "426588",
                    "all",
                ]
            },
        }
        cursor_partner_deals = col_partner_deals.find(query_partner_deals)
        # for doc in cursor_partner_deals:
        #     print(doc)

    @task(118)
    def search_tags(self) -> None:
        query_ops_config = {"key": "default-tags"}
        tag = col_ops_configs_plo.find_one(query_ops_config)
        # print(tag)

    @task(1465)
    def stop(self) -> None:
        self.interrupt()


class MongoUser(User):
    wait_time = between(0, 2)
    tasks = [EcommBehaviour, PloBehaviour]
