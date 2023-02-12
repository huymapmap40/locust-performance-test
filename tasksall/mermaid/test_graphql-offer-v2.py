import json
import sys
from locust import HttpUser, TaskSet, task, between
from random import randint
import base64
import logging
from gql_response import Offer, Offers, Campaign, Category, Merchants

class UserBehavior(TaskSet):

    offers_range = (99711, 103791)
    account_range = (650000001, 650000050)

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        accountId = randint(*self.account_range)
        headerStr = json.dumps({"id": accountId, "uuid": "mockuuid13fw3342fw"}).encode('utf-8')
        header = base64.b64encode(headerStr)
        base64_message = header.decode('utf-8')

        self.headers = {
            'X-Shopback-Domain': 'www.shopback.sg',
            'X-Shopback-Agent': 'sbiosagent/1.0',
            'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
            'X-Shopback-Client-User-Agent': 'Locust test',
            'Accept': 'application/graphql',
            'Authorization': 'JWT ' + base64_message
        }

    def _get_func_name(self):
        return sys._getframe(1).f_code.co_name

    def _call_graphql(self, query, name='others'):
        with self.client.post(
                url='/graphql?test={}'.format(name),
                name=name,
                json={"query": query},
                headers=self.headers,
                catch_response=True
        ) as res:
            data = json.loads(res.text)
            if data.get('errors'):
                res.failure(json.dumps(data['errors']))
                logging.error(json.dumps(data))
        self.client.close()

    @task(3)
    def get_offers_by_merchant_id(self):
        query = f'''
        {{
          offers(offersQueryInput: {{merchantId:2, size:30}}) {Offers} 
          merchants {Merchants}
        }}
        '''
        self._call_graphql(query, self._get_func_name())

    @task(2)
    def get_offer_by_offer_id(self):
        offer_id = randint(156749, 156775)
        query = f'''
        {{
          offer(offerId: {offer_id}) {Offer} 
          merchants {Merchants}
        }}
        '''
        self._call_graphql(query, self._get_func_name())

    @task(3)
    def get_follow_offers(self):
        query = f'''
        {{
        followOffers(followOffersQueryInput: {{
          page: 0,
          size: 30
        }}) {Offers}
        followOffersMerchant {Merchants}
        followOffersSubcategory {Category}
        }}
        '''
        self._call_graphql(query, self._get_func_name())

    @task(6)
    def get_offers_by_label_id(self):
        page = randint(0, 18)
        query = f"""
        {{
          offers(offersQueryInput: {{labelId:2, size:30, page:{page}}}) {Offers}
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

    @task(3)
    def get_campaign_offers(self):
        query = f"""
        {{
          offers(offersQueryInput: {{sortBy: "price", campaignId: 38}}) {Offers}
          campaign(campaignId: 38) {Campaign}
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

    @task(6)
    def get_search_offers(self):
        query = f"""
        {{
          searchOffers(searchOffersQueryInput: {{keyword: "糖果", size: 30}}) {Offers}
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

    @task(2)
    def get_search_recommend_offers(self):
        query = f"""
        {{
          searchRecommendOffers {Offers}
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

    @task(6)
    def get_offer_carousel_recommendation(self):
        query = f"""
        {{
          recommendOffers(recommendOffersQueryInput: {{queryName: "offer_carousel", limit: 15}}) {Offers}
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

    @task(3)
    def get_merchant_carousel_recommendation(self):
        query = f"""
        {{
          recommendOffers(recommendOffersQueryInput: {{
            queryName: "merchant_carousel",
            limit: 15,
            tag: "9557b334642414950ad1c8e3aeeb8c68"
          }}) {Offers} 
          merchants {Merchants}
        }}
        """
        self._call_graphql(query, self._get_func_name())

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.5, 1)
