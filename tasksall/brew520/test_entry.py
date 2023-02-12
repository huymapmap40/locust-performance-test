# Testing Steps Locally
# 1. run locust in root of the repo: ./scripts/local_start.sh internal-staging-au-orca-es7-1191401129.ap-southeast-1.elb.amazonaws.com:9200/au-raw-product-data-loadtest test_entry tasksall/brew520

# Testing Steps On K8S
# 1. Deploy: ./install.sh environments/test_brew520.yaml tasksall/brew520 locust-brew520 sb-dep-dev-team-orca
# 2. Testing: ./forward.sh sb-dep-dev-team-orca
# 3. Destroy: ./remove.sh sb-dep-dev-team-orca

from locust import HttpUser, task, between
import random
import json


def readJson(fileName):
    with open(fileName, 'r') as f:
        content = f.read()
        return json.loads(content)


keywords = [
    # top 50
    'amazon',            'myer',          'ebay',
    'iconic',            'target',        'david_jones',
    'shein',             'kmart',         'the_iconic',
    'booking.com',       'catch',         'big_w',
    'chemist_warehouse', 'jb_hi-fi',      'apple',
    'bonds',             'harvey_norman', 'cotton_on',
    'uber_eats',         'kogan',         'booking',
    'woolworths',        'good_guys',     'nike',
    'coles',             'adore_beauty',  'petbarn',
    'aliexpress',        'agoda',         'asos',
    'pet_circle',        'bunnings',      'adairs',
    'officeworks',       'sephora',       'airbnb',
    'catch_of_the_day',  'uniqlo',        'bws',
    'doordash',          'jb_hifi',       'rebel',
    'mecca',             'expedia',       'menulog',
    'h_m',               'dan_murphy',    'iherb',
    'groupon',           'jd_sports',
    # high recall
    'a', 'air', 'book', 'c', 'travel'
]


class SimulatedUserAction(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def task(self):
        keyword = random.choice(keywords)
        url = '/_msearch'
        headers = {
            "Content-Type": "application/x-ndjson",
            "Authorization": "Basic b3JjYS1kZXY6S2FwRXdsU3JBZW9N"
        }
        queries = readJson("/locust-tasks/%s.json" % keyword)
        data = "%s,\n%s,\n%s,\n%s\n" % (
            json.dumps(queries['body'][0]),
            json.dumps(queries['body'][1]),
            json.dumps(queries['body'][2]),
            json.dumps(queries['body'][3])
        )
        with self.client.get(
                url, headers=headers, name=keyword, data=data, catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if result["responses"][0]["_shards"]["failed"] != 0:
                    response.failure("response[0] _shard fails: %s" % keyword)
                elif result["responses"][1]["_shards"]["failed"] != 0:
                    response.failure("response[1] _shard fails: %s" % keyword)
                else:
                    response.success()
            else:
                response.failure("wrong response status(%s): %s: " % (
                    response.status_code, keyword) + json.dumps(response.json()['error']))
