import os
import sys
import random
import string
import uuid
import json
import logging
from json import dumps
from base64 import b64encode
from enum import Enum
from locust import HttpUser, task, between
from dotenv import load_dotenv

load_dotenv()

class Platform(Enum):
  IOS = 'ios'
  ANDROID = 'android'
  WEB = 'web'

with open(os.path.join(sys.path[0], 'config.json')) as f:
  data = json.load(f)

PHONE_NUMBER_OFFSET_UPPER_BOUND = 8999999
PHONE_NUMBER_BASE = 990000000
APP_BUILD_NUMBER = '4000000'

##########################################################
## Make sure you select the right environment variables ##
##########################################################
env = os.getenv('ENVIRONMENT', default='staging-sg')
env_vars = data['ENV_VARS'][env]
##########################################################

def random_headers():
  platform = random.choice(list(Platform))
  if (platform == Platform.IOS):
    sb_agent = 'sbiosagent/4.0.0'
    user_agent = str(uuid.uuid4()).upper()
    build_no = APP_BUILD_NUMBER
  elif (platform == Platform.ANDROID):
    sb_agent = 'sbandroidagent/4.0.0'
    user_agent = ''.join(random.choice(string.hexdigits) for _ in range(16)).lower()
    build_no = APP_BUILD_NUMBER
  else:
    sb_agent = 'sbconsumeragent/1.0'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.{}.{} Safari/537.{}'.format(
      random.randint(1, 999), random.randint(1, 999), random.randint(1, 999)
    )
    build_no = ''

  ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
  return {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': env_vars['domain'],
    'X-Shopback-Agent': sb_agent,
    'X-Shopback-Client-User-Agent': user_agent,
    'X-Shopback-Member-Ip-Address': ip_address,
    'X-Shopback-Build': build_no,
    'X-Shopback-Recaptcha-Type': 'bypass'
  }

# Users who signed in on start and will access member service with JWT token
class SignInUser(HttpUser):
  wait_time = between(0.3, 3)
  weight = 50

  def on_start(self):
    index = random.randint(env_vars['accounts']['min_index'], env_vars['accounts']['max_index'])
    # index = random.randint(17000, 17999) for staging-sg kyc data test
    self.email = env_vars['accounts']['pattern'].format(index=index)
    self.client.headers = random_headers()
    self.sign_in()

  @task(30)
  def oauth_validate(self):
    self.client.post('/members/v2/oauth/validate', json={})

  @task(8)
  def get_profile(self):
    self.client.get(
      '/members/v3/me?type=mobile',
      name='/members/v3/me?type=mobile'
    )

  # @task(5)
  def get_kyc_context(self):
    self.client.get('/members/me/kyc/context')

  @task(4)
  def refresh_token(self):
    self.client.post('/members/me/refresh-jwt-token', json={})

  def check_unique_email(self):
    url = '/members/check-unique?email={email}'
    with self.client.get(url.format(email=self.email), name=url, catch_response=True) as resp:
      if resp.status_code == 409 or resp.status_code == 200:
        resp.success()

  def sign_in(self):
    # simulate the Ray ID of Cloudflare, this is used as the requestId
    self.client.headers['cf-ray'] = ''.join(random.choice(string.hexdigits) for _ in range(20)).lower()
    payload = {
      'email': self.email,
      'password': env_vars['accounts']['password']
    }
    resp = self.client.post('/members/sign-in', json=payload, name='/members/sign-in')
    body = resp.json()
    self.client.headers['X-Shopback-JWT-Access-Token'] = body['auth']['access_token']
    self.client.headers['X-Shopback-Member-Refresh-Token'] = body['auth']['refresh_token']
    self.client.headers['Authorization'] = 'JWT {}'.format(body['auth']['access_token'])

  @task
  def sign_in_flow(self):
    self.client.post('/members/me/sign-out', json={})
    self.check_unique_email()
    self.sign_in()

  # @task
  def refresh_kyc_context(self):
    self.client.put('/members/me/kyc/context', json={})

# ShopBack internal clients (other ShopBack teams)
class InternalClient(HttpUser):
  wait_time = between(0.1, 0.3)
  weight = 1

  def on_start(self):
    self.client.headers = {
      'Content-Type': 'application/json',
      'X-Shopback-Domain': env_vars['domain'],
      'X-Shopback-Agent': 'sbconsumeragent/1.0',
      'X-Shopback-Member-Operator': 'risk-service'
    }

  def random_account_id(self):
    # the old_ids of 1111load+test{id}@shopback.com accounts
    return random.randint(env_vars['accounts']['min_old_id'], env_vars['accounts']['max_old_id'])

  def check_get_profile_response(self, response):
    # because some old_ids in the range above are empty
    # (The range contains 16,173 numbers but there are only 15k accounts)
    # the error code 50002 (user id not found) is also an correct response
    if response.status_code == 200:
      # success
      response.success()
    elif response.status_code == 400:
      body = response.json()
      if body['error']['code'] == 50002:
        # user not found
        response.success()

  def check_get_kyc_response(self, response):
    # because some old_ids in the range above are empty
    # (The range contains 16,173 numbers but there are only 15k accounts)
    # the error code 10069 (get kyc context error) is also an correct response for user id not found case
    if response.status_code == 200:
      # success
      response.success()
    elif response.status_code == 422:
      body = response.json()
      if body['error']['code'] == 10069 and body['error']['message'] == 'cannot find the user':
        # user not found
        response.success()

  @task(10)
  def get_kyc_context_by_id(self):
    account_id = self.random_account_id()
    url = '/int/members/{id}/kyc/context'
    with self.client.get(url.format(id=account_id), name=url, catch_response=True) as response:
      self.check_get_kyc_response(response)

  @task(10)
  def get_profile_by_id(self):
    account_id = self.random_account_id()
    url = '/int/members/{id}'
    with self.client.get(
      url.format(id=account_id) + '?referrer=1&phoneNumber=1&address=1',
      name=url,
      catch_response=True
    ) as response:
      self.check_get_profile_response(response)

  @task
  def get_profile_by_token(self):
    account_id = self.random_account_id()
    token = b64encode(dumps({'id': account_id}).encode('utf-8')).decode('utf-8')
    self.client.headers['Authorization'] = 'JWT {}'.format(token)
    url = '/int/members'
    with self.client.get(
      url + '?referrer=1&phoneNumber=1&address=1',
      name=url,
      catch_response=True
    ) as response:
      self.check_get_profile_response(response)

# Sign Up Users
class SignUpUser(HttpUser):
  wait_time = between(0.1, 3)
  weight = 1

  def on_start(self):
    self.mobile_country_code = '886'
    self.otp_code = '123456'
    self.client.headers = random_headers()

  def random_datas(self):
    self.email = 'coral.test.signup_{}@shopback.com'.format(str(uuid.uuid4()).replace('-', ''))
    number_offset = random.randint(0, PHONE_NUMBER_OFFSET_UPPER_BOUND)
    self.mobile_number = str(PHONE_NUMBER_BASE + number_offset)

  def start_session(self):
    payload = {
      'email': self.email,
      'mobile_country_code': self.mobile_country_code,
      'mobile_number': self.mobile_number,
      'target': 'signup'
    }
    resp = self.client.post('/members/v2/otp/session', json=payload)
    data = resp.json()
    self.session_id = data['session_id']
    self.channel = 'sms'
    if data['auto_select_item_id']:
      self.channel = data['auto_select_item_id']
    else:
      self.channel = data['channel_list'][0]

  def send_otp(self):
    payload = {
      'session_id': self.session_id,
      'channel': self.channel,
      'otp': self.otp_code
    }
    resp = self.client.post('/members/v2/otp', json=payload)
    data = resp.json()
    self.otp_request_id = data['request_id']

  def verify_otp(self):
    payload = {
      'session_id': self.session_id,
      'request_id': self.otp_request_id,
      'otp': self.otp_code
    }
    self.client.post('/members/v2/otp/verification', json=payload)

  def validate_email(self):
    payload = {
      'email': self.email
    }
    self.client.get('/members/v2/email/validation', json=payload)

  def sign_up(self):
    payload = {
      'authentication_type': 'email',
      'email': self.email,
      'mobile_country_code': self.mobile_country_code,
      'mobile': self.mobile_number,
      'password': 'Abcd1234',
      'otp_request_id': self.otp_request_id,
      'full_name': 'coral loadtest'
    }
    with self.client.post('/members/v2/sign-up', json=payload, catch_response=True) as resp:
      body = resp.json()
      if resp.status_code == 201 or (resp.status_code == 400 and body['error']['code'] == 10016):
        resp.success()
      else:
        logging.error('payload: {}\nbody: {}'.format(dumps(payload), dumps(body)))

  @task
  def sign_up_flow(self):
    self.random_datas()
    self.start_session()
    self.send_otp()
    self.verify_otp()
    self.validate_email()
    self.sign_up()
