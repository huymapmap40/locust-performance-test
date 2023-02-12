import base64

def jwt(account_id: int):
    account = f'{{"id":{account_id},"uuid":"u"}}'
    encoded_bytes = base64.b64encode(account.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str


def get_user_headers_by_account_id(account_id: int):
    if not account_id:
        raise RuntimeError(f"Invalid account id given: {account_id}")

    headers = {
        "X-Shopback-Agent": "sbandroidagent/1.0",
        "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
        "X-Shopback-Build": "3200000",
        "Authorization": f"JWT {jwt(account_id)}",
    }
    return headers
