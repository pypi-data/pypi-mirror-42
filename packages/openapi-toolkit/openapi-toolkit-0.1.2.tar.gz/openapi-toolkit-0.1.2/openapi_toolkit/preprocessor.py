import inspect
import re

from mako.template import Template, ModuleInfo, _get_module_info
from mako.lookup import TemplateLookup


def indent(text, *args):
    """Indent filter for Mako that matches template indention"""
    _, module_name, line_no, *_ = inspect.stack()[1]
    module_info = _get_module_info(module_name)
    module_source, template_source = module_info.code, module_info.source

    source_map = ModuleInfo.get_module_source_metadata(
        module_source,
        full_line_map=True
    )

    line_map = source_map['full_line_map']
    template_ln_no = line_map[line_no - 1]
    template_line = template_source.split('\n')[template_ln_no - 1]

    indent = re.match('[ \t]*', template_line).group(0)
    return indent.join(x for x in text.splitlines(keepends=True))


class MakoPreprocessor(object):
    """Mako Preprocessor Handler"""
    def __init__(self, directories=None, module_directory=None):
        self.lookup = None
        if directories:
            self.lookup = TemplateLookup(
                directories=directories,
                module_directory=module_directory,

            )

    def handle(self, raw):
        """Contractual handle method"""
        return Template(
            text=raw,
            lookup=self.lookup,
        ).render()
