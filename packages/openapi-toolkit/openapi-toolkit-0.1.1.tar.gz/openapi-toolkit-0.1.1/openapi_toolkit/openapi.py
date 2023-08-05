from alchemize import Attr, JsonModel

from openapi_toolkit import yaml
from openapi_toolkit.resolver import resolve_spec
from openapi_toolkit.schemas import validate_spec

http_codes = [
    '100', '101', '102',

    '200', '201', '202', '203', '204', '205', '206', '207', '208', '226',

    '300', '301', '302', '303', '304', '305', '307', '308',

    '400', '401', '402', '403', '404', '405', '406', '407', '408', '409',
    '410', '411', '412', '413', '414', '415', '416', '417', '418', '422',
    '423', '424', '428', '429', '431', '451',

    '500', '501', '502', '503', '504', '505', '507', '508', '511',
]


class Parameter(JsonModel):
    __mapping__ = {
        'name': Attr('name', str),
        'in': Attr('location', str),
        'description': Attr('description', str),
        'required': Attr('required', bool),
        'deprecated': Attr('deprecated', bool),
        'schema': Attr('schema', dict),
    }


class Response(JsonModel):
    __mapping__ = {
        'summary': Attr('summary', str),
        'description': Attr('description', str),
        'headers': Attr('headers', dict),
        'content': Attr('content', dict),
    }


class Responses(JsonModel):
    __mapping__ = {
        http_code: Attr('http_{}'.format(http_code), Response)
        for http_code in http_codes
    }


class Operation(JsonModel):
    __mapping__ = {
        'tags': Attr('tags', list),
        'summary': Attr('summary', str),
        'description': Attr('description', str),
        'operationId': Attr('operation_id', str),
        'parameters': Attr('parameters', [Parameter]),
        'responses': Attr('responses', Responses),
    }


class Path(JsonModel):
    __mapping__ = {
        'summary': Attr('summary', str),
        'description': Attr('description', str),
        'get': Attr('get', Operation),
        'put': Attr('put', Operation),
        'patch': Attr('patch', Operation),
        'post': Attr('post', Operation),
        'delete': Attr('delete', Operation),
        'head': Attr('head', Operation),
        'options': Attr('options', Operation),
        'trace': Attr('trace', Operation),
    }


class OpenAPI(object):
    """OpenAPI Specification Manager"""
    def __init__(self, filename, spec):
        self.filename = filename
        self.specification = spec

    def find_path(self, path, method=None):
        """Searches for Path data (incomplete)"""
        path_data = self.specification['paths'].get(path)

        if method:
            return Operation.from_dict(path_data.get(method))

        return Path.from_dict(path_data)

    def find_input_schema(self, path, method, content_type):
        """Searches for a request body schema by path, method, and content_type"""
        data = (
            self.specification['paths']
            .get(path, {})
            .get(method, {})
            .get('requestBody', {})
            .get('content', {})
            .get(content_type, {})
            .get('schema')
        )
        if not data:
            raise KeyError(
                'Could not locate schema with path={}, method={}, '
                'content_type={}'.format(path, method, content_type)
            )
        return data

    @classmethod
    def load(cls, filename, preprocessor=None, resolve=True, validate=True):
        """Loads an OpenAPI Specification from a file"""
        with open(filename) as fp:
            raw = fp.read()

            if preprocessor:
                raw = preprocessor.handle(raw)

            data = yaml.load(raw)

            if resolve:
                data = resolve_spec(data)

            if validate:
                validate_spec(data)

            return cls(filename, data)

    def save(self, filename):
        """Save the loaded OpenAPI specification to a file"""
        with open(filename, 'w') as fp:
            yaml.dump(self.specification, stream=fp)
