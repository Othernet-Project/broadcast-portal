from . import Option


class Version(Option):
    @property
    def version_string(self):
        return '{name} {ver}'.format(name=self.exts.name,
                                     ver=self.exts.version)

    def add_args(self):
        self.parser.add_argument('--version', action='version',
                                 version=self.version_string)
