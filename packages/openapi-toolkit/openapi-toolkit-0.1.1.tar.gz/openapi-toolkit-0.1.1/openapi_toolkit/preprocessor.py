from mako.template import Template
from mako.lookup import TemplateLookup


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
