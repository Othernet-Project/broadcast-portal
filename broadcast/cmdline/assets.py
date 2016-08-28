import os
import sys
import shutil
import signal
import tempfile
import subprocess
from os.path import join, abspath

from . import Command
from ..app.exts import container as exts
from ..util.skinning import skin_dir


TMPDIR = tempfile.gettempdir()
COMPASS_PID = join(TMPDIR, 'compass.pid')
COFFEE_PID = join(TMPDIR, 'coffee.pid')
COMPASS = shutil.which('compass')
COFFEE = shutil.which('coffee')


class AssetsCommand(object):
    """
    Base class for assets-related commands
    """
    def __init__(self):
        config = exts.config
        skin_path = exts.skin_path
        if skin_path:
            self.skindir = abspath(skin_path)
        else:
            self.skindir = skin_dir()
        print("using skin in '{}'".format(self.skindir))
        self.static_url = config['assets.url']
        self.srcdir = join(self.skindir, 'src')
        self.assetsdir = join(self.skindir, 'assets')
        self.scssdir = join(self.srcdir, 'scss')
        self.csdir = join(self.srcdir, 'coffee')
        self.cssdir = join(self.assetsdir, 'css')
        self.jsdir = join(self.assetsdir, 'js')
        self.imgdir = join(self.assetsdir, 'img')
        self.fontdir = join(self.assetsdir, 'font')

    def compass_cmd(self, *cmds):
        return (COMPASS,) + cmds + (
            '--http-path', self.static_url,
            '--app-dir', self.skindir,
            '--sass-dir', self.scssdir,
            '--css-dir', self.cssdir,
            '--images-dir', self.imgdir,
            '--fonts-dir', self.fontdir,
            '--javascript-dir', self.jsdir,
            '--output-style', 'expanded',
            '--relative-assets',
        )

    def coffee_cmd(self, *cmds):
        return (COFFEE,) + cmds + (
            '--bare',
            '--output', self.jsdir,
            self.csdir,
        )


def write_pid(pid, pidfile):
    with open(pidfile, 'w') as f:
        f.write(str(pid))


def read_pid(pidfile):
    with open(pidfile, 'r') as f:
        return int(f.read())


def kill_pid(pid):
    if sys.platform == 'win32':
        # On win32, a cmd.exe is spawned, which then spawns the process, so
        # the pid is for the cmd.exe process and not the main process
        # itself. Therefore we need to send an interrupt to the cmd.exe
        # process which will then hopefully terminate the children.
        os.kill(pid, signal.CTRL_BREAK_EVENT)
    os.kill(pid, signal.SIGTERM)


def kill_pidfile(pidfile):
    pid = read_pid(pidfile)
    kill_pid(pid)
    os.unlink(pidfile)


def start_watchers():
    print('starting watchers')
    cmd = AssetsCommand()
    if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP'):
        # On Windows, commands are run in a subshell regardless of the
        # ``shell`` argument unless CREATE_NEW_PROCESS_GROUP flag is used.
        # This flag is not supported on *nix platforms, so we test that the
        # flag is supposed instead of testing for platform.
        popen_kw = dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        popen_kw = {}
    compass = subprocess.Popen(cmd.compass_cmd('watch'), **popen_kw)
    coffee = subprocess.Popen(cmd.coffee_cmd('--watch'), **popen_kw)
    write_pid(compass.pid, COMPASS_PID)
    write_pid(coffee.pid, COFFEE_PID)
    sys.exit(0)


def recompile_assets():
    print('recompiling assets')
    cmd = AssetsCommand()
    try:
        subprocess.check_call(cmd.compass_cmd('compile', '--force'))
        subprocess.check_call(cmd.coffee_cmd('--compile'))
    except subprocess.CalledProcessError:
        print('Error compiling assets')
        sys.exit(1)
    else:
        sys.exit(0)


class Watch(Command):
    name = 'watch'
    help = 'watch a skin directory for changes and recompile assets'

    def add_args(self):
        self.group.add_argument('--skin-path', '-P', metavar='PATH',
                                help='use PATH instead of skin specified by '
                                'the configuration file')

    def run(self, args):
        exts.skin_path = args.skin_path
        self.exts.add_hook('pre_start', start_watchers)


class StopWatchers(Command):
    name = 'stop-watchers'
    help = 'stop the assets watchers'

    @staticmethod
    def kill_process(name, pidfile):
        try:
            kill_pidfile(pidfile)
        except FileNotFoundError:
            print('{} PID file not found, nothing to do'.format(name))
        except OSError:
            print('{} could not be stopped, is it still running?'.format(name))
            os.unlink(pidfile)

    def run(self, args):
        print('stopping watchers')
        self.kill_process('compass', COMPASS_PID)
        self.kill_process('coffee', COFFEE_PID)
        self.quit(0)


class Recompile(Command):
    name = 'recompile'
    help = 'recompile assets'

    def add_args(self):
        self.group.add_argument('--skin-path', '-P', metavar='PATH',
                                help='use PATH instead of skin specified by '
                                'the configuration file')

    def run(self, args):
        exts.skin_path = args.skin_path
        self.exts.add_hook('pre_start', recompile_assets)
