import pprint
from os.path import abspath, join

from confloader import ConfDict

from . import Option


DEFAULT_PID = '/var/run/broadcast.pid'


class Conf(Option):
    def add_args(self):
        default_conf = abspath(join(self.exts.root, 'broadcast.ini'))
        self.exts.default_conf = default_conf
        self.parser.add_argument('--conf', '-c', metavar='PATH',
                                 default=default_conf,
                                 help='set the configuration file path')
        self.parser.add_argument('--debug-conf', action='store_true',
                                 help='print out the configuration options '
                                 'and quit')

    def test(self, args):
        return True

    def run(self, args):
        self.conf.update(ConfDict.from_file(args.conf))
        if args.debug_conf:
            print('Using file: {}'.format(args.conf))
            pprint.pprint(self.conf, indent=4)
            self.quit(0)
