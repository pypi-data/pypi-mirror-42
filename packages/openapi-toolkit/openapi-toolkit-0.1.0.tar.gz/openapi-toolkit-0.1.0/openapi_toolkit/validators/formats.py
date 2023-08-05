import uuid

from openapi_toolkit.validators import schema_format


@schema_format.checks('uuid', ValueError)
def uuid_format(value):
    return uuid.UUID(value)
