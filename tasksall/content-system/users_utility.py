import base64

def jwt(account_id: int, uuid: str):
    account = f'{{"id":{account_id},"uuid":"{uuid}"}}'
    encoded_bytes = base64.b64encode(account.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str


def get_user_auth_header(account_id: int, uuid: str):
    if not account_id:
        raise RuntimeError(f"Invalid account id given: {account_id}")

    return f"JWT {jwt(account_id, uuid)}"
