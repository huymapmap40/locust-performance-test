from random import choice, sample

from locust import HttpUser, between, tag, task

from base import AppTestBase, WebTestBase
from users_utility import get_user_auth_header
from users import testing_users
from entities import sboc_baseline_merchant_ids, sboc_upsize_merchant_ids, online_paylater_merchant_ids, instore_pay_outlet_ids, instore_paylater_outlet_ids

class TestApp(AppTestBase):
    def on_start(self):
        super(TestApp, self).on_start()

    @task(1)
    def test_instore_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1339;
        self.load_component_content(component_id)

    @task(1)
    def test_sboc_baseline_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1340;
        self.load_component_content(component_id)


    @task(1)
    def test_sboc_upsized_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1341;
        self.load_component_content(component_id)

  
    @task(1)
    def test_sboc_deal_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1342;
        self.load_component_content(component_id)


    @task(1)
    def test_sboc_coupon_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1343;
        self.load_component_content(component_id)


    @task(1)
    def test_online_paylater_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1344;
        self.load_component_content(component_id)
    
    @task(4)
    def test_combined_banner_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1345;
        self.load_banner_content(component_id)

    @task(4)
    def test_combined_banner_content_two(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1368;
        self.load_banner_content(component_id)

    @task(4)
    def test_deal_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1366;
        self.load_banner_content(component_id)

    @task(4)
    def test_deal_content_two(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1369;
        self.load_banner_content(component_id)

    @task(4)
    def test_coupon_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1367;
        self.load_banner_content(component_id)

    @task(4)
    def test_coupon_content_two(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        component_id = 1370;
        self.load_banner_content(component_id)

class TestDynamicContent(AppTestBase):
    def on_start(self):
        super(TestDynamicContent, self).on_start()

    @task(1)
    def test_sboc_baseline_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        entity_ids = sample(sboc_baseline_merchant_ids, 10)
        component_map_id = 334;
        self.load_dynamic_content(component_map_id, entity_ids)


    @task(1)
    def test_sboc_upsized_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        entity_ids = sample(sboc_upsize_merchant_ids, 3) # we only have 6 upsize merchants in staging sadly
        component_map_id = 336;
        self.load_dynamic_content(component_map_id, entity_ids)

    @task(0)
    def test_instore_pay_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        entity_ids = sample(instore_pay_outlet_ids, 10)
        component_map_id = 310;
        self.load_dynamic_content(component_map_id, entity_ids)

    @task(0)
    def test_instore_paylater_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        entity_ids = sample(instore_paylater_outlet_ids, 10)
        component_map_id = 312;
        self.load_dynamic_content(component_map_id, entity_ids)

    @task(0)
    def test_online_paylater_content(self):
        user = choice(testing_users)
        self.headers['Authorization'] = get_user_auth_header(user['id'], user['uuid'])
        entity_ids = sample(online_paylater_merchant_ids, 10)
        component_map_id = 313;
        self.load_dynamic_content(component_map_id, entity_ids)

  
class User(HttpUser):
    tasks = [
      # TestApp, 
      TestDynamicContent
    ]
    wait_time = between(0.5, 1.5)
