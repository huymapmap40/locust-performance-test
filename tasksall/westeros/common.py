BASE_URL = 'https://staging.shopback.sg'

GATEWAY_URL = 'https://gateway-staging.shopback.sg'

AGENTS = ['sbconsumeragent/1.0', 'sbandroidagent/1.0', 'sbiosagent/1.0']

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopback-Domain': 'www.shopback.sg',
    'X-Shopback-Agent': 'sbconsumeragent/1.0',
    'X-Shopback-Key': 'q452R0g0muV3OXP8VoE7q3wshmm2rdI3',
    'X-Shopback-Client-User-Agent': 'Locust test',
    'X-Shopback-Recaptcha-Type': 'bypass',
    'X-shopback-internal': '682a46b19b953306c9ee2e8deb0dc210',
}

CREDENTIALS = {
    'email': 'roran.lai@shopback.com',
    'password': 'ShopBack123'
}

MERCHANT = [
    {
        "MERCHANT_ID": 19352,
        "MERCHANT_SHORTNAME": 'lazada'
    },
    {
        "MERCHANT_ID": 19160,
        "MERCHANT_SHORTNAME": 'nike'
    }
]
CAMPAIGN = 'auto-test'


def sign_in(self, tag):
    global COOKIES
    payload = CREDENTIALS
    response = self.client.post(
        url=f'{GATEWAY_URL}/members/sign-in', headers=HEADERS, json=payload,
        name=f'{tag} - /members/sign-in')
    COOKIES = {
        'sbet': response.json()['auth']['access_token'],
        'sbrefresh': response.json()['userTokens']['refreshToken']['id'],
        'sbaccess': response.json()['userTokens']['accessToken']['id']
    }
    return response
