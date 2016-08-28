from os.path import abspath, join

from . import Command


CONFIGURATION_TEMPLATE = """[config]

defaults =
  {path}

# Add your settings below this line
"""


class CustomConf(Command):
    name = 'custom-conf'
    help = 'create custom configuration file skeleton'

    def add_args(self):
        self.group.add_argument('confpath', metavar='PATH', help='output path')

    def run(self, args):
        output_path = args.confpath
        print('writing configuration to {}'.format(output_path))
        with open(output_path, 'w') as f:
            f.write(CONFIGURATION_TEMPLATE.format(path=self.exts.default_conf))
        self.quit(0)
