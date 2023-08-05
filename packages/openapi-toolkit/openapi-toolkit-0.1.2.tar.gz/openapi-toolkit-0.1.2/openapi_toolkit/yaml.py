import io

from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter


class CustomRepresenter(RoundTripRepresenter):
    def ignore_aliases(self, _data):
        return True


def load(data):
    yaml = YAML()
    yaml.Representer = CustomRepresenter
    return yaml.load(data)


def dump(data, stream=None):
    if not stream:
        stream = io.StringIO()

    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.Representer = CustomRepresenter

    res = yaml.dump(data, stream=stream)

    if isinstance(stream, io.StringIO):
        res = stream.getvalue()

    return res
