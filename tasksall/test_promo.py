from random import randint, uniform
from base64 import b64encode
from datetime import datetime
from time import sleep
from uuid import uuid4
from locust import TaskSet, HttpUser, task, between
from utility_users import get_unique_account_id

class UserBehaviour(TaskSet):
    account_id = 0
    auth_header = ""
    cashback_offset = 0
    items = []
    items_with_id = []
    payment_method = {}
    internal_key = ""

    def jwt(self, account_id: int) -> str:
        account = f'{{"id":{account_id}}}'
        encoded_bytes = b64encode(account.encode("utf-8"))
        encoded_str = str(encoded_bytes, "utf-8")
        return f"JWT {encoded_str}"

    def on_start(self) -> None:
        self.account_id = get_unique_account_id() # randint(1, 20000)
        self.auth_header = self.jwt(self.account_id)
        self.cashback_offset = 1
        self.items = [{
            "amount": 101,
            "merchant": {
                "id": "9607bab0-3de5-4e81-a590-4fb17bc876be",
                "type": "sbpaylater-merchant",
            },
            "businessUnit": "sbpaylater"
        }]
        self.items_with_id = [{
            "id": "item-one",
            "amount": 101,
            "merchant": {
                "id": "9607bab0-3de5-4e81-a590-4fb17bc876be",
                "type": "sbpaylater-merchant",
            },
            "businessUnit": "sbpaylater"
        }]
        self.payment_method = {
            "type": "card",
            "bin": "111111",
        }
        self.internal_key = "63ef0310-b1a3-4bed-aafd-61cab6d88c8f"

    @task(1)
    def just_browsing(self) -> None:
        now = datetime.today().isoformat()
        headers = {
            'x-shopback-agent': 'sbiosagent',
            'authorization': self.auth_header,
        }
        fetched = []
        next = None
        while (True):
            search_data = {
                "filters": {
                    "redemptionsRemaining": {
                        "gt": 0,
                    },
                    "campaign": {
                        "redeemFrom": {
                            "lt": now,
                        },
                        "redeemBy": {
                            "gt": now,
                        },
                        "redemptionPercent": {
                            "lt": 100,
                        },
                    },
                },
                "sort": {
                    "by": "claimedAt",
                    "order": "desc",
                },
                "transformerVersion": 0,
            }

            if next:
                search_data["next"] = next

            with self.client.post(
                url="/promo/claims/search",
                headers=headers,
                json=search_data,
                catch_response=True,
            ) as search_res:
                if not search_res:
                    break

                search_json = search_res.json()
                # print(search_json)
                search_res.close()

                if (
                    "data" not in search_json
                    or "claims" not in search_json["data"]
                ):
                    raise RuntimeError(f"Unsuccessful response: {search_json}")
            
                claims = search_json["data"]["claims"]
                fetched.extend(claims)

                if "next" in search_json["data"]:
                    next = search_json["data"]["next"]

                if ("next" not in search_json["data"] or not len(claims)):
                    break

            sleep(uniform(1, 5)) # human user delay

        if not fetched:
            return

        campaign_id = fetched[randint(0, len(fetched) - 1)]["campaignId"] # check not empty
        campaign_data = {
            "transformerVersion": 0,
        }

        with self.client.post(
            name = "/promo/campaigns/:id/details",
            url=f"/promo/campaigns/{campaign_id}/details",
            headers=headers,
            json=campaign_data,
            catch_response=True,
        ) as campaign_res:
            # print(campaign_res.json())
            campaign_res.close()

    @task(1)
    def checking_out(self) -> None:
        now = datetime.today().isoformat()
        headers = {
            'x-shopback-agent': 'sbiosagent',
            'authorization': self.auth_header,
        }

        # fetch eligible (truncated) claims
        eligibility_input = {
            "payment": {
                "cashbackOffset": self.cashback_offset,
                "paymentMethod": self.payment_method,
            },
            "items": self.items,
        }
        fetched = []
        next = None
        while (True):
            search_data = {
                "eligibility": {
                    "input": eligibility_input
                },
                "filters": {
                    "redemptionsRemaining": {
                        "gt": 0,
                    },
                    "campaign": {
                        "businessUnits": [
                            "sbpaylater"
                        ],
                        "redeemFrom": {
                            "lt": now,
                        },
                        "redeemBy": {
                            "gt": now,
                        },
                        "redemptionPercent": {
                            "lt": 100,
                        },
                    },
                },
                "sort": {
                    "by": "claimedAt",
                    "order": "desc",
                },
                "transformerVersion": 0,
            }

            if next:
                search_data["next"] = next

            with self.client.post(
                url="/promo/claims/search",
                headers=headers,
                json=search_data,
                catch_response=True,
            ) as search_res:
                if not search_res:
                    break

                search_json = search_res.json()
                # print(search_json)
                search_res.close()

                if (
                    "data" not in search_json
                    or "claims" not in search_json["data"]
                ):
                    raise RuntimeError(f"Unsuccessful response: {search_json}")
            
                claims = search_json["data"]["claims"]
                fetched.extend(claims)

                if "next" in search_json["data"]:
                    next = search_json["data"]["next"]

                if ("next" not in search_json["data"] or not len(claims)):
                    break

            sleep(uniform(1, 5)) # human user delay

        # print(len(fetched))

        # fetch ineligible (truncated) claims
        next = None
        while (True):
            search_data = {
                "eligibility": {
                    "input": eligibility_input,
                    "failedRestrictionCategories": [
                        "item",
                        "aggregatedItems",
                    ],
                },
                "filters": {
                    "redemptionsRemaining": {
                        "gt": 0,
                    },
                    "campaign": {
                        "businessUnits": [
                            "sbpaylater"
                        ],
                        "redeemFrom": {
                            "lt": now,
                        },
                        "redeemBy": {
                            "gt": now,
                        },
                        "redemptionPercent": {
                            "lt": 100,
                        },
                    },
                },
                "sort": {
                    "by": "claimedAt",
                    "order": "desc",
                },
                "transformerVersion": 0,
            }

            if next:
                search_data["next"] = next

            with self.client.post(
                url="/promo/claims/search",
                headers=headers,
                json=search_data,
                catch_response=True,
            ) as search_res:
                if not search_res:
                    break

                search_json = search_res.json()
                # print(search_json)
                search_res.close()

                if (
                    "data" not in search_json
                    or "claims" not in search_json["data"]
                ):
                    raise RuntimeError(f"Unsuccessful response: {search_json}")
            
                claims = search_json["data"]["claims"]

                if "next" in search_json["data"]:
                    next = search_json["data"]["next"]

                if ("next" not in search_json["data"] or not len(claims)):
                    break

            sleep(uniform(1, 5)) # human user delay

        if not fetched:
            return

        # uncommited redemption
        claim_id = fetched[randint(0, len(fetched) - 1)]["_id"] # check not empty
        redemption_uncommitted_data = {
            "claimId": claim_id,
            "accountId": self.account_id,
            "cashbackOffset": self.cashback_offset,
            "paymentMethod": self.payment_method,
            "items": self.items_with_id,
            "commit": False,
        }
        headers = {
            "x-api-key": self.internal_key
        }

        with self.client.post(
            url="/promo/redemptions",
            headers=headers,
            json=redemption_uncommitted_data,
            catch_response=True,
        ) as redemption_uncommitted_res:
            if not redemption_uncommitted_res:
                return

            # print(redemption_uncommitted_res.json())
            if redemption_uncommitted_res.status_code == 422:
                # might have run out of redemptions
                redemption_uncommitted_res.success()
                redemption_uncommitted_res.close()
                return
            redemption_uncommitted_res.close()

        sleep(uniform(1, 5)) # human user delay

        # committed redemption
        claim_id = fetched[randint(0, len(fetched) - 1)]["_id"]
        client_reference = str(uuid4())
        redemption_committed_data = {
            "claimId": claim_id,
            "accountId": self.account_id,
            "cashbackOffset": self.cashback_offset,
            "paymentMethod": self.payment_method,
            "items": self.items_with_id,
            "commit": True,
            "reference": client_reference,
        }

        with self.client.post(
            url="/promo/redemptions",
            headers=headers,
            json=redemption_committed_data,
            catch_response=True,
        ) as redemption_committed_res:
            if not redemption_committed_res:
                return

            # print(redemption_committed_res.json())
            if redemption_committed_res.status_code == 422:
                # might have run out of redemptions
                redemption_committed_res.success()
                redemption_committed_res.close()
                return
            redemption_committed_res.close()

            # confirm redemption
            redemption_update_data = {
                "identifierType": "clientReference",
                "clientReference": client_reference,
                "status": "redeemed",
            }

            with self.client.put(
                url="/promo/redemptions",
                headers=headers,
                json=redemption_update_data,
                catch_response=True,
            ) as redemption_update_res:
                # print(redemption_update_res.status_code)
                redemption_update_res.close()

class PromoUser(HttpUser):
    wait_time = between(3, 10)
    tasks = [UserBehaviour]
