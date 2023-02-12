import os
from redis import Redis
import base64
from typing import Dict
from locust import HttpUser
from uuid import uuid4

redisHost = os.environ["REDIS_HOST"]
r = Redis(host=redisHost, port=6379)


# account-ids must first be added: see ../redis-users/README.md


def get_unique_account_id() -> int:
    account_id = r.spop("account-ids")
    if not account_id:
        return 0
    else:
        return int(account_id.decode("utf8"))


def jwt(account_id: int) -> str:
    account = f'{{"id":{account_id},"uuid":"testuuid"}}'
    encoded_bytes = base64.b64encode(account.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str


def get_user_headers_by_account_id(account_id: int) -> Dict[str, str]:
    if not account_id:
        raise RuntimeError(f"Invalid account id given: {account_id}")

    headers = {
        "X-Shopback-Agent": "sbandroidagent/3.72.0-SNAPSHOT",
        "X-Shopback-Uid": "1889B3C1-DD0D-40A5-876D-0BFC72142C2E",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "User-Agent": "ShopBack/3.72.0-SNAPSHOT (com.shopback.app; build:2820000; Android 10; Android SDK built for x86 google generic_x86) okhttp/4.7.2",
        "X-Shopback-Build": "99999999999",
        "Authorization": f"JWT {jwt(account_id)}",
        "Content-Type": "application/json",
        "X-Shopback-Agent": "sbandroidagent/1.0",
        "X-Shopback-Client-User-Agent": "ac1e01f1dc111223",
        "X-Device-Id": "46c483100e9f1826",
        "X-Shopback-Device-Model": "Android",
        "Cf-Connecting-Ip": "127.0.0.10",
    }
    return headers


# account-emails must first be added: see ../redis-users/README.md


def get_unique_email() -> str:
    email = None

    while not email:
      email = r.spop("account-emails")
      if email:
        break

    return email.decode("utf8")


def get_user_headers_by_login(
    locustUser: HttpUser, email: str, password: str
) -> Dict[str, str]:
    if not email:
        raise RuntimeError(f"Invalid email given: {email}")

    if not password:
        raise RuntimeError(f"Invalid password given: {password}")

    headers_sign_in = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Shopback-Agent": "sbconsumeragent/1.0",
        "X-Shopback-Internal": "682a46b19b953306c9ee2e8deb0dc210",
        "X-Shopback-Client-User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Cookie": "__cfduid=d0f5e6ac2e2bc790f5221a905493f13c01573390581; __cfduid=d31969f13afed883c0379993ec5d5ea081598507902",
        "X-Shopback-Recaptcha-Type": "bypass",
    }

    payload = {"email": email, "password": password}
    res_login = locustUser.client.post(
        url="/members/sign-in",
        json=payload,
        headers=headers_sign_in,
    )

    credentials = res_login.json()  # expires in an hour

    res_login.close()

    if (
        "auth" not in credentials
        or "access_token" not in credentials["auth"]
        or "userTokens" not in credentials
        or "accessToken" not in credentials["userTokens"]
        or "id" not in credentials["userTokens"]["accessToken"]
    ):
        raise RuntimeError(f"Error logging in with email: {email}, credentials: {credentials}")

    jwt = credentials["auth"]["access_token"]
    member_token = credentials["userTokens"]["accessToken"]["id"]

    req_headers = {
        "X-Shopback-Domain": "www.shopback.sg",
        "X-Shopback-Language": "en",
        "X-Request_Id": str(uuid4()),
        "X-Device-Id": "46c483100e9f1826",
        "X-Shopback-Client-User-Agent": "46c483100e9f1826",
        "X-Shopback-Device-Model": "Android",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Agent": "sbandroidagent/3.72.0-SNAPSHOT",
        "X-Shopback-Uid": "1889B3C1-DD0D-40A5-876D-0BFC72142C2E",
        "User-Agent": "ShopBack/3.72.0-SNAPSHOT (com.shopback.app; build:2820000; Android 10; Android SDK built for x86 google generic_x86) okhttp/4.7.2",
        "X-Shopback-Build": "3720000",
        "X-Shopback-Store-Service": "true",
        "Authorization": "JWT " + jwt,
        "Content-Type": "application/json; charset=UTF-8",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "X-Shopback-Member-Access-Token": member_token,
        "Cookie": "__cfduid=d3b45e39bcf454e5f7bea047b14a12b0d1572501016",
    }

    # # optionally attempt to align concurrent start of task execution
    # # 2 different approaches

    # # # (1) check redis
    # # wait = 1
    # # while wait == 1:
    # #     # time.sleep(1)
    # #     wait = r.exists("account-emails")

    # # (2) start task execution after delay
    # # observed to perform better
    # now = time.time()
    # target = 1605004500
    # time.sleep(target - now)

    return req_headers
