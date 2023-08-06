import json
import os
import pytest


def read_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


@pytest.fixture(scope='module')
def sample_json_output():
    return read_json_data(os.path.join('easyparse', 'data', 'output.json'))
