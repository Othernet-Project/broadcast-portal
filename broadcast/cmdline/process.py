from __future__ import print_function

import os
import sys
import signal

from . import Option, Command


DEFAULT_PID = '/var/run/broadcast.pid'


class Startup(Option):
    def add_args(self):
        group = self.parser.add_argument_group('startup options')
        if hasattr(os, 'fork'):
            group.add_argument('--background', '-b', action='store_true',
                               help='run in background')
            group.add_argument('--pid-file', '-p', metavar='PATH',
                               default=DEFAULT_PID, help='create a PID file '
                               'at specified path (default is '
                               '{})'.format(DEFAULT_PID))
            group.add_argument('--user', '-U', metavar='USER',
                               help='user to use for the process')
            group.add_argument('--group', '-G', metavar='GROUP',
                               help='group to use for the process')
        else:
            group.set_defaults(background=False, pid_file=None, user=None,
                               group=None)
        group.add_argument('--debug', action='store_true',
                           help='whether to enable debugging')
        group.add_argument('--quiet', '-q', action='store_true',
                           help='suppress terminal output')

    def test(self, args):
        return True

    def run(self, args):
        user_default = self.conf.get('app.user')
        group_default = self.conf.get('app.group')
        debug_default = self.conf.get('app.debug', False)
        self.exts.debug = args.debug or debug_default
        self.exts.quiet = args.quiet or args.command is not None
        if hasattr(os, 'fork'):
            self.exts.proc_config = {
                'background': args.background,
                'pid_file': args.pid_file,
                'user': args.user or user_default,
                'group': args.group or group_default,
            }
        else:
            self.exts.proc_config = {
                'background': False,
                'pid_file': None,
                'user': None,
                'group': None,
            }


class Stop(Command):
    name = 'stop'
    help = 'stop the process that would be started with given options'

    def run(self, args):
        with open(args.pid_file, 'r') as f:
            pid = f.read()
        try:
            os.kill(int(pid), signal.SIGTERM)
        except (ValueError, TypeError):
            print('Invalid pid in pid file: {}'.format(pid), file=sys.stderr)
            self.quit(1)
        except Exception as e:
            print('Could not stop the app: {}'.format(e))
            self.quit(1)
        self.quit(0)
