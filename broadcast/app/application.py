import os
import sys
import time
import logging
import importlib

from bottle import Bottle
from gevent import pywsgi
from confloader import ConfDict
from greentasks.scheduler import TaskScheduler

from . import exts
from . import cmdline
from .. import __version__
from ..util.signal_handlers import on_interrupt

try:
    import pwd
    import grp
except ImportError:
    has_user = False
else:
    has_user = True


class Application:
    LOOP_INTERVAL = 5  # in seconds

    def __init__(self, root):
        self.name = 'broadcast'
        self.version = __version__
        self.root = root
        self.work_dir = os.getcwd()
        self.server = None
        self.app = Bottle()
        self.child = False
        self.hooks = {
            'pre_init': [],
            'pre_start': [],
            'post_stop': [],
            'background': [],
        }
        self.config = ConfDict({
            'autojson': True,
            'catchall': True,
        })
        self.app.config = self.config

        self.exts = exts.container
        self.exts.name = self.name
        self.exts.version = self.version
        self.exts.root = root
        self.exts.config = self.config
        self.exts.app = self.app
        self.exts.template_defaults = {}
        self.exts.tasks = TaskScheduler()
        self.exts.add_hook = self.add_hook_fn

        # Parse command line arguments and execute any option handlers and
        # commands
        self.exts.cmdline = cmdline.parse_args()

        self.debug = self.exts.debug

        # Register all application hooks
        for hook_group in self.hooks.keys():
            hook_conf_key = 'stack.{}'.format(hook_group)
            self.add_hooks(hook_group, self.config.get(hook_conf_key, []))

        # Run pre-init hooks
        self.run_hooks('pre_init')

        # Register application components
        self.add_plugins(self.config['stack.plugins'])
        self.add_routes(self.config['stack.routes'])

        # Register interrupt handler
        on_interrupt(self.halt)

    def add_hooks(self, hook_group, hooks):
        if hooks is None:
            return
        for hook in hooks:
            self.add_hook_fn(hook_group, self._import(hook))

    def add_hook_fn(self, hook_group, fn):
        self.hooks[hook_group].append(fn)

    def run_hooks(self, hook_group):
        for hook in self.hooks[hook_group]:
            hook()

    def add_plugins(self, plugins):
        for plugin in plugins:
            plugin = self._import(plugin)
            self.app.install(plugin())

    def add_routes(self, routing):
        for route in routing:
            route = self._import(route)
            for r in route():
                r.route(app=self.app)

    def debug_app(self):
        logging.debug('============ DEBUG ===========')
        logging.debug('Registered hooks:')
        for hook_group, hooks in self.hooks.items():
            for hook in hooks:
                logging.debug('%-10s %s.%s', hook_group, hook.__module__,
                              hook.__name__)
        logging.debug('Registered routes:')
        for r in self.app.routes:
            logging.debug("%-30s %-4s %s <%s>", r.name, r.method, r.rule,
                          r.callback.__name__)
        logging.debug('==============================')

    def fork(self):
        """
        Attempt to fork the current process

        Raises ``RuntimeError`` if the fork is not successful.
        """
        try:
            pid = os.fork()
        except OSError:
            raise RuntimeError('process failed to fork')
        if pid == 0:
            if not self.child:
                os.setsid()
        else:
            os._exit(0)
        return pid

    def setuid(self):
        """
        Set user and group ID of the process

        If ``self.group`` is not defined, then this method uses the group ID of
        the ``self.user``.

        Returns a tuple containing the active user and group IDs.
        """
        if not has_user:
            logging.warn('User switching is disabled on this OS')
            return
        user = self.exts.proc_conf['user']
        group = self.exts.proc_conf['group']
        logging.debug('Setting process UID and GID')
        pwinfo = pwd.getpwnam(user)
        uid = pwinfo.pw_uid
        os.setuid(uid)
        os.seteuid(uid)
        if group:
            logging.debug('Using specified group for GID')
            gid = grp.getgrpnam(group).grp_gid
        else:
            logging.debug('Using specified user for GID')
            gid = pwinfo.pw_gid
        os.setgid(gid)
        os.setegid(gid)
        logging.debug('Process UID=%s and GID=%s', uid, gid)
        return uid, gid

    def daemonize(self):
        """
        Background the process in which the app instance is initialized

        This method converts the process to which this instance belongs, to a
        double-forking daemon.

        This method returns the current PID of the forked child process.
        """
        logging.info('Forking into background')
        # Fork once
        try:
            self.fork()
        except RuntimeError:
            logging.critical('Could not fork the process')
            sys.exit(1)
        logging.debug('Started child process')
        self.child = True
        # Set up the process environment
        os.chdir(os.path.normpath(self.work_dir))
        os.umask(0)
        # Fork second time
        try:
            self.fork()
        except RuntimeError:
            logging.critical('Could not double-fork the process')
            sys.exit(1)
        logging.debug('Running as daemon (PID={})'.format(os.getpid()))
        # Write the PID as needed
        pid_file = self.exts.proc_conf['pid_file']
        if pid_file:
            with open(pid_file, 'w') as f:
                f.write(str(os.getpid()))
            logging.debug('PID file written to %s', pid_file)
        # Switch to unprivileged user
        if self.exts.proc_conf['user']:
            self.setuid()

    def start(self):
        self.run_hooks('pre_start')
        if self.debug:
            self.debug_app()
        if self.exts.proc_conf['background']:
            self.daemonize()
        host = self.config['server.bind']
        port = self.config['server.port']
        self.server = pywsgi.WSGIServer((host, port), self.app, log=None)
        self.server.start()  # non-blocking
        assert self.server.started, 'Expected server to be running'
        logging.info("Started server on http://%s:%s/", host, port)
        self.init_background()

    def init_background(self):
        while True:
            time.sleep(self.LOOP_INTERVAL)
            self.run_hooks('background')

    def halt(self):
        logging.info('Stopping the application')
        self.server.stop(5)
        logging.info('Running pre-stop hooks')
        self.run_hooks('post_stop')

    @staticmethod
    def _import(name):
        mod, obj = name.rsplit('.', 1)
        mod = importlib.import_module(mod)
        return getattr(mod, obj)
