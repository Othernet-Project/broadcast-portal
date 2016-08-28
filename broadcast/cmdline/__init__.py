import sys

from ..app.exts import container as exts


class ArgBase(object):
    def __init__(self, parser):
        self.parser = parser
        self.exts = exts
        self.conf = exts.config
        self.add_args()

    def add_args(self):
        pass

    def run(self, args):
        pass

    @staticmethod
    def quit(code=0):
        sys.exit(code)


class Option(ArgBase):
    def test(self, args):
        return False


class Command(ArgBase):
    name = None
    help = None

    def __init__(self, parser):
        self.group = parser.add_argument_group(
            '{} command options'.format(self.name))
        super(Command, self).__init__(parser)


class DummyCommand(object):
    def __init__(self, parser):
        pass

    def run(self, args):
        pass
