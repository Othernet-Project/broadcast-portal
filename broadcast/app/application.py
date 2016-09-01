import os
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


class Application:
    LOOP_INTERVAL = 5  # in seconds

    def __init__(self, root):
        self.name = 'broadcast'
        self.version = __version__
        self.root = root
        self.server = None
        self.app = Bottle()
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
        self.add_tasks(self.config['stack.tasks'])

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

    def add_tasks(self, tasks):
        for task_path in tasks:
            task_cls = self._import(task_path)
            self.exts.tasks.schedule(task_cls)

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

    def start(self):
        self.run_hooks('pre_start')
        if self.debug:
            self.debug_app()
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
