import json
from os.path import join, dirname
from functools import partial


def read_fixture_file(handler, filename):
    file_path = join(dirname(__file__), filename)
    with open(file_path) as f:
        data = handler(f)
    return data


load_fixtures = partial(read_fixture_file, lambda x: [i.strip() for i in x])
load_json_fixtures = partial(read_fixture_file, lambda x: json.load(x))
