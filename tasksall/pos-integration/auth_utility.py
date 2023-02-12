import hmac
import hashlib
import json


def generate_hmac_signature(params: object, accessKeySecret: str): 
    payload = compute_request_payload(params);
    signature = hmac.new(accessKeySecret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature



def compute_request_payload(params: object):
    body_digest = create_sha256_digest(params['body']);
    return params['method'].upper() + "\n" + params['contentType'] + "\n" + params['timestamp'] + "\n" + params['pathWithQuery'] + "\n" + body_digest


def create_sha256_digest(body: object): 
    if (bool(body) == False):
      return ''

    sorted_keys = sorted(body);
    sorted_body_dict = {}
    for key in sorted_keys:
        sorted_body_dict[key] = body[key]

    hash = hashlib.sha256()
    stringifiedBody = json.dumps(sorted_body_dict, separators=(',', ':'))
    hash.update(stringifiedBody.encode('utf-8'));
    return hash.hexdigest()