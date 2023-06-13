import json

import jsonschema

from consts import Encodings


def validate_schema(file, schema):
    try:
        jsonschema.validate(file, schema)
    except jsonschema.exceptions.ValidationError:
        return False
    else:
        return True


def json_to_dict(file):
    with open(file, "r", encoding=Encodings.UTF8) as test_data_file:
        test_data = json.load(test_data_file)
    return test_data
