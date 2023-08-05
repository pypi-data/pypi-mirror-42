import json
import os

import jsonschema


def load_validation_schema(version='3.0'):
    filename = os.path.join(
        os.path.dirname(__file__),
        '{}.json'.format(version)
    )

    with open(filename) as fp:
        return json.load(fp)


def validate_spec(spec):
    schema = load_validation_schema()
    jsonschema.validate(spec, schema)
