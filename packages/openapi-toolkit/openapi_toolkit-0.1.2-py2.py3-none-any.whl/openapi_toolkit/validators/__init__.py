import jsonschema
from jsonschema.exceptions import FormatError, ValidationError

schema_format = jsonschema.FormatChecker()


def expanded_format(validator, format, instance, schema):
    if validator.format_checker is not None:
        try:
            validator.format_checker.check(instance, format)

        except ValidationError as error:
            yield error

        except FormatError as error:
            yield ValidationError(error.message, cause=error.cause)


class JsonSchema(object):
    def __init__(self, formats=None, validators=None):
        self.CustomValidator = jsonschema.validators.create(
            meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
            validators={
                **jsonschema.Draft4Validator.VALIDATORS,
                'format': expanded_format,
                **(validators or {}),
            }
        )

    def validate(self, schema, value):
        """Validates a value against a schema defintion"""
        validator = self.CustomValidator(schema, format_checker=schema_format)
        return validator.validate(value)


from .formats import *  # NOQA
