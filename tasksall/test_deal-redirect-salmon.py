from locust import HttpUser, TaskSet, task
import random
import json


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.headers = {
            'Authorization': 'Bearer eyJ1dWlkIjoiMzMyNUY0OUJCRTZCNDM0MDlDMTlBQUM3MjIwRUY0REMiLCJpc3MiOiJ3d3cuc2hvcGJhY2suc2ciLCJpc3N1ZWRBdCI6MTU5MzQxNDIwNS45NzQsImlhdCI6MTU5MzQxNDIwNSwiZXhwIjoxNTkzNTAwNjA1LCJpZCI6MjM0OTN9',
            'Content-Type': 'application/json',
            'X-Shopback-Agent': 'sbiosagent/2.8.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Internal': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Request-ID': 'f022449e-b9dd-4485-8e4d-7b6aa5e5a871',
            'X-Shopback-Build': '2369700',
            'X-Shopback-Domain': 'www.shopback.sg',
        }

        self.storeAffiliateIds = [64765, 83677, 187689, 187690, 187691, 251343, 251344, 251345,
                                  56689, 56820,  62394,  62395,  62396,  62397,  62398,  63238,
                                  64813, 64814,  64815,  64816,  64817,  64818,  68809,  70539,
                                  70780, 70781,  71218,  71219,  71590,  72928,  73195,  73823,
                                  74522, 74523,  74542,  74595,  74852,  75299,  76020,  76493,
                                  76533, 76534,  76583,  76584,  76585,  76689,  76968,  76998,
                                  76999, 77001,  77002,  77202,  77273,  77274,  77586,  77660,
                                  78986, 79565,  79755,  79756,  80054,  80856,  80857,  80858,
                                  80859, 80860,  80861,  80862,  80863,  80864,  80865,  80866,
                                  80867, 80868,  80869,  80870,  81088,  81251,  81581,  81582,
                                  81583, 81584,  81585,  81586,  81587,  81588,  81589,  81590,
                                  81591, 81592,  81593,  81594,  81595,  81596,  81597,  81598,
                                  81599, 81600,  82307,  82308]
        self.storeAffiliateId = random.choice(self.storeAffiliateIds)

    @task
    def dealRedirect(self):
        self.client.post(
            url='/mobile/stores/redirect/' + str(self.storeAffiliateId),
            headers=self.headers)


class WebsiteUser(HttpUser):
    tasks =  [UserBehavior]
    min_wait = 1000
    max_wait = 1000
