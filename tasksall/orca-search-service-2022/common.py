import csv, json, base64
from os.path import join, dirname
from functools import partial

# Please ensure the country you would like to test
COUNTRY = "AU" # TW, ID, SG, AU, PH, MY, VN, TH


DOMAINS = {
    "TW": "www.shopback.com.tw",
    "AU": "www.shopback.com.au",
    "ID": "www.shopback.co.id"
}

ACCOUNT_IDS = {
    "TW": 2464051,
    "AU": 506518,
    "ID": 4957484
}

UUIDS = {
    "TW": "827aa9d38e4f4608ac609d6c41332dc2",
    "AU": "555d8093f9d3491cb730908af6bbf23d",
    "ID": "04f2acdbc551465b9fe0046cc5673217"
}

DOMAIN = DOMAINS[COUNTRY]
ACCOUNT_ID = ACCOUNT_IDS[COUNTRY]
UUID = UUIDS[COUNTRY]

def generate_jwt_token(account_id):
    authorization_content = json.dumps({
        "uuid": UUID,
        "iss": DOMAIN,
        "issuedAt": 1577477107.184, 
        "iat": 1577477107,
        "exp": 2077477107, # Nov 01 2035
        "id": account_id
    })
    encoded_auth = base64.b64encode(authorization_content.encode("utf-8"))
    access_token = str(encoded_auth, 'utf-8')
    return access_token

def readCSV(fileName):
    with open(fileName, 'r') as f:
        r = csv.reader(f)
        # next(r)  # skip header line
        return list(r)
    
def read_fixture_file(handler, filename):
    file_path = join(dirname(__file__), filename)
    with open(file_path) as f:
        data = handler(f)
    return data

load_fixtures = partial(read_fixture_file, lambda x: [i.strip() for i in x])

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopback-Agent": "sbiosagent/1.0",
    "X-Shopback-Key": "q452R0g0muV3OXP8VoE7q3wshmm2rdI3",
    "X-Shopback-Store-Service": "true",
    "X-Shopback-Country": COUNTRY,
    "x-Shopback-domain": DOMAIN,
    "x-shopback-client-user-agent": "test",
    "X-Shopback-Recaptcha-Type": "bypass",
    "X-Shopback-Build": "3770000",
    "Authorization": 'JWT {}'.format(generate_jwt_token(ACCOUNT_ID)) 
}