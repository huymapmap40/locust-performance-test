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

class Platform(Enum):
  IOS = 'ios'
  ANDROID = 'android'
  WEB = 'web'

SIGN_IN_BASE = 990999000
SIGN_UP_BASE = 990910000

def random_headers():
  platform = random.choice(list(Platform))
  if (platform == Platform.IOS):
    sb_agent = 'sbiosagent/3.30.0'
    user_agent = str(uuid.uuid4()).upper()
    build_no = '9900000'
  elif (platform == Platform.ANDROID):
    sb_agent = 'sbandroidagent/3.30.0'
    user_agent = ''.join(random.choice(string.hexdigits) for _ in range(16)).lower()
    build_no = '9900000'
  else:
    sb_agent = 'sbconsumeragent/1.0'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.{}.{} Safari/537.{}'.format(
      random.randint(1, 999), random.randint(1, 999), random.randint(1, 999)
    )
    build_no = ''

  ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
  return {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.sg',
    'X-Shopback-Agent': sb_agent,
    'X-Shopback-Client-User-Agent': user_agent,
    'X-Shopback-Member-Ip-Address': ip_address,
    'X-Shopback-Build': build_no,
    'X-Shopback-Recaptcha-Type': 'bypass'
  }

def start_session_from_user(user, target):
  payload = {
    'mobile_country_code': user.mobile_country_code,
    'mobile_number': user.mobile_number,
    'target': target
  }
  resp = user.client.post('/members/v2/otp/session', json=payload)
  data = resp.json()
  user.session_id = data['session_id']
  if data['auto_select_item_id']:
    user.channel = data['auto_select_item_id']
  else:
    user.channel = data['channel_list'][0]

def send_otp_from_user(user):
  payload = {
    'session_id': user.session_id,
    'channel': user.channel,
    'otp': user.otp_code
  }
  resp = user.client.post('/members/v2/otp', json=payload)
  data = resp.json()
  user.otp_request_id = data['request_id']

def verify_otp_from_user(user):
  payload = {
    'session_id': user.session_id,
    'request_id': user.otp_request_id,
    'otp': user.otp_code
  }
  user.client.post('/members/v2/otp/verification', json=payload)

# Mobile Sign Up Users
class SignUpUser(HttpUser):
  wait_time = between(1, 3)
  weight = 1

  def on_start(self):
    self.mobile_country_code = '886'
    self.otp_code = '123456'
    self.client.headers = random_headers()
    self.number_offset = 0

  def random_datas(self):
    self.mobile_number = SIGN_UP_BASE + self.number_offset
    self.number_offset = self.number_offset + 1

  def start_session(self):
    start_session_from_user(self, 'signup')

  def send_otp(self):
    send_otp_from_user(self)

  def verify_otp(self):
    verify_otp_from_user(self)

  def sign_up(self):
    payload = {
      'mobile_country_code': self.mobile_country_code,
      'mobile': self.mobile_number,
      'otp_request_id': self.otp_request_id,
      'full_name': 'coral loadtest'
    }
    with self.client.post('/members/v3/sign-up/mobile', json=payload, catch_response=True) as resp:
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
    self.sign_up()

# Mobile Sign In Users

class SignInUser(HttpUser):
  wait_time = between(0.1, 1)
  weight = 5

  def on_start(self):
    self.mobile_country_code = '886'
    self.otp_code = '123456'
    self.client.headers = random_headers()
    self.number_offset = 0

  def random_datas(self):
    self.mobile_number = str(SIGN_IN_BASE + random.randint(0, 500))

  def start_session(self):
    start_session_from_user(self, 'mobile_signin')

  def send_otp(self):
    send_otp_from_user(self)

  def verify_otp(self):
    verify_otp_from_user(self)

  def sign_in(self):
    payload = {
      'otp_request_id': self.otp_request_id,
    }
    with self.client.post('/members/v2/sign-in/mobile', json=payload, catch_response=True) as resp:
      body = resp.json()
      if resp.status_code == 200:
        resp.success()
      else:
        logging.error('payload: {}\nbody: {}'.format(dumps(payload), dumps(body)))

  @task
  def sign_in_flow(self):
    self.random_datas()
    self.start_session()
    self.send_otp()
    self.verify_otp()
    self.sign_in()

