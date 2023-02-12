from pymongo import MongoClient
import random
from datetime import datetime
from locust import TaskSet, User, task, between

STAGING_SG_SBOC_MONGO_URI = ""
if not STAGING_SG_SBOC_MONGO_URI:
    raise AssertionError("Please specify STAGING_SG_SBOC_MONGO_URI")

sboc_mongo_client = MongoClient(STAGING_SG_SBOC_MONGO_URI)

db_challenge = sboc_mongo_client.challenge
col_challenges = db_challenge.challenges
col_challenges_partnerships = db_challenge["challenges-partnerships"]

accounts = [
    3771390,
    3926369,
    4995337,
    3482392,
    1339538,
    3826888,
    124549,
    3568308,
    10213,
    3235233,
    101811,
    2562585,
    181983,
    2421219,
    876757,
    22459,
    3500726,
    2608908,
    3927673,
    1474861,
]

codes = [
    "AU_NOV_SBOC_SURFSTITCH_NC_AUD5",
    "AU_NOV_SBOC_SURFSTITCH_EC_AUD2_50",
    "SG_NOV_SBOC_SPEND_SAFRAMEMBERS_SGD1",
    "SG_NOV_SBOC_IHERB_UOBNOV2020_SGD1",
    "SG_OCT_SBOC_SPEND_PASSIONCARD_SGD2",
    "SG_NOV_SBOC_2STORES_PASSIONCARD_SGD4",
]


# queries specified in https://shopadmin.atlassian.net/wiki/spaces/HG/pages/1309278853/11.11+Challenge


class UserBehaviour(TaskSet):
    account_id = 0

    def on_start(self) -> None:
        self.account_id = random.choice(accounts)

    @task(1)
    def first_aggregation(self) -> None:
        now = datetime.now()

        pipeline = [
            {
                "$match": {
                    "code": {"$in": codes},
                    "type": "LIMITED_TIME",
                    "isPrivate": True,
                    "isOffline": False,
                    "$or": [
                        {"startAt": {"$lte": now}},
                        {"listingTime": {"$lte": now}},
                    ],
                    "endAt": {"$gte": now},
                    "entryConditionCheckType": "foreground",
                }
            },
            {
                "$lookup": {
                    "from": "challenges-accounts",
                    "let": {"id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$accountId", self.account_id]},
                                        {"$eq": ["$challengeId", "$$id"]},
                                    ],
                                }
                            }
                        }
                    ],
                    "as": "account",
                }
            },
            {
                "$unwind": {
                    "path": "$account",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "code": 1,
                    "entryConditions": 1,
                    "entryConditionCheckType": 1,
                    "account.accountId": 1,
                    "account.status": 1,
                }
            },
            {"$match": {"account.accountId": {"$exists": False}}},
        ]

        cursor_challenges = col_challenges.aggregate(pipeline)
        # for doc in cursor_challenges:
        #     print(doc)

    @task(1)
    def second_aggregation(self) -> None:
        now = datetime.now()

        pipeline = [
            {
                "$match": {
                    "source": {"$in": ["shopback", None]},
                    "$or": [
                        {"isOffline": False},
                        {"debugModeEnabled": True, "debugUsers": self.account_id},
                    ],
                }
            },
            {
                "$lookup": {
                    "from": "challenges-accounts",
                    "let": {"id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$accountId", self.account_id]},
                                        {"$eq": ["$challengeId", "$$id"]},
                                    ],
                                }
                            }
                        }
                    ],
                    "as": "account",
                }
            },
            {
                "$unwind": {
                    "path": "$account",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "code": 1,
                    "headline": 1,
                    "title": 1,
                    "subTitle": 1,
                    "type": 1,
                    "ctaTitle": 1,
                    "ctaLink": 1,
                    "logo": 1,
                    "bannerUrl": 1,
                    "startAt": 1,
                    "endAt": 1,
                    "expirationWaitingDays": 1,
                    "participantLimit": 1,
                    "currentParticipants": 1,
                    "rewardLimit": 1,
                    "currentRewards": 1,
                    "status": 1,
                    "reward": 1,
                    "goals": 1,
                    "goalType": 1,
                    "inQueue": 1,
                    "isPrivate": 1,
                    "rank": 1,
                    "showOnList": 1,
                    "listingTime": 1,
                    "debugModeEnabled": 1,
                    "debugUsers": 1,
                    "account.goals": 1,
                    "account.reward": 1,
                    "account.status": {"$ifNull": ["$account.status", "NOT_STARTED"]},
                    "account.accountId": 1,
                    "account.updatedAt": 1,
                    "account.rankStatus": {"$ifNull": ["$account.rankStatus", 30]},
                }
            },
            {
                "$match": {
                    "$or": [
                        {
                            "$and": [
                                {"account.status": "REWARD_ISSUED"},
                                {"account.updatedAt": {"$gt": now}},
                            ],
                        },
                        {
                            "account.status": {
                                "$in": [
                                    "NOT_STARTED",
                                    "OPTED_IN",
                                    "IN_PROGRESS",
                                    "ACTION_COMPLETED",
                                    "GOAL_COMPLETED",
                                ],
                            },
                        },
                    ],
                }
            },
            {
                "$match": {
                    "$or": [
                        {
                            "startAt": {"$lte": now},
                            "listingTime": None,
                            "showOnList": None,
                        },
                        {"showOnList": True, "listingTime": {"$lte": now}},
                        {"account.accountId": {"$exists": True}},
                        {"debugModeEnabled": True, "debugUsers": self.account_id},
                    ]
                }
            },
            {
                "$match": {
                    "$or": [
                        {"account.accountId": {"$exists": True}},
                        {"participantLimit": None, "rewardLimit": None},
                        {"participantLimit": 0, "rewardLimit": 0},
                        {
                            "participantLimit": {"$gt": 0},
                            "$expr": {
                                "gt": ["$participantLimit", "$currentParticipants"]
                            },
                        },
                        {
                            "rewardLimit": {"$gt": 0},
                            "$expr": {"gt": ["$rewardLimit", "$currentRewards"]},
                        },
                        {"debugModeEnabled": True, "debugUsers": self.account_id},
                    ]
                }
            },
            {
                "$match": {
                    "$or": [
                        {"isPrivate": False},
                        {"isPrivate": True, "account.accountId": {"$exists": True}},
                        {"isPrivate": True, "code": {"$in": codes}},
                        {"debugModeEnabled": True, "debugUsers": self.account_id},
                    ]
                }
            },
            {
                "$match": {
                    "$or": [
                        {"endAt": {"$gte": now}},
                        {"account.accountId": {"$exists": True}, "endAt": {"$lt": now}},
                        {"debugModeEnabled": True, "debugUsers": self.account_id},
                    ]
                }
            },
            {
                "$addFields": {
                    "groupStatus": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$in": [
                                            {
                                                "$ifNull": [
                                                    "$account.status",
                                                    "NOT_STARTED",
                                                ]
                                            },
                                            ["NOT_STARTED"],
                                        ]
                                    },
                                    "then": 1,
                                },
                                {
                                    "case": {
                                        "$in": [
                                            "$account.status",
                                            ["OPTED_IN", "IN_PROGRESS"],
                                        ]
                                    },
                                    "then": 2,
                                },
                                {
                                    "case": {
                                        "$in": [
                                            "$account.status",
                                            [
                                                "ACTION_COMPLETED",
                                                "GOAL_COMPLETED",
                                                "REWARD_ISSUED",
                                            ],
                                        ]
                                    },
                                    "then": 3,
                                },
                            ],
                            "default": 4,
                        }
                    }
                }
            },
            {
                "$facet": {
                    "challenges": [
                        {"$sort": {"groupStatus": 1, "rank": 1}},
                        {"$skip": 0},
                        {"$limit": 100},
                    ],
                    "total": [{"$count": "count"}],
                }
            },
        ]

        cursor_challenges = col_challenges.aggregate(pipeline)
        # for doc in cursor_challenges:
        #     print(doc)

    @task(1)
    def third_aggregation(self) -> None:
        now = datetime.now()

        pipeline = [
            {
                "$match": {
                    "source": {"$in": ["shopback", None]},
                    "type": "LIMITED_TIME",
                    "isPrivate": True,
                    "isOffline": False,
                    "$or": [
                        {"startAt": {"$lte": now}},
                        {"listingTime": {"$lte": now}},
                    ],
                }
            },
            {
                "$lookup": {
                    "from": "challenges-accounts",
                    "let": {"id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$accountId", self.account_id]},
                                        {"$eq": ["$challengeId", "$$id"]},
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "account",
                }
            },
            {"$unwind": {"path": "$account", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 1,
                    "code": 1,
                    "entryConditions": 1,
                    "entryConditionCheckType": 1,
                    "account.accountId": 1,
                    "account.status": 1,
                }
            },
            {"$match": {"account.accountId": {"$exists": False}}},
        ]

        cursor_challenges = col_challenges.aggregate(pipeline)
        # for doc in cursor_challenges:
        #     print(doc)

    @task(1)
    def find(self) -> None:
        query_challenges_partnerships = {"challengeCodes": random.choice(codes)}
        cursor_challenges_partnerships = col_challenges_partnerships.find(
            query_challenges_partnerships
        )
        # for doc in cursor_challenges_partnerships:
        #     print(doc)


class MongoUser(User):
    wait_time = between(0, 2)
    tasks = [UserBehaviour]
