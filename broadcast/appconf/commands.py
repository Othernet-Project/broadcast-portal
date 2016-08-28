"""
commands.py: Command line arg handlers

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import getpass
import sys

from ..models.auth import User
from ..plugins.static import rebuild_assets
from ..app.exts import container as exts

try:
    raw_input
except NameError:
    raw_input = input


COMMANDS = dict()


def command(name):
    def _command(func):
        COMMANDS[name] = func
        return func
    return _command


@command('su')
def create_superuser():
    print("Press ctrl-c to abort")
    databases = exts.databases
    try:
        username = raw_input('Username: ')
        email = raw_input('Email: ')
        password = getpass.getpass()
    except (KeyboardInterrupt, EOFError):
        print("Aborted")
        sys.exit(1)

    try:
        User.new(username=username,
                 password=password,
                 email=email,
                 is_superuser=True,
                 confirmed=datetime.datetime.utcnow(),
                 db=databases.sessions,
                 overwrite=True)
        print("User created.")
    except User.AlreadyExists:
        print("User already exists, please try a different username.")
        create_superuser()
    except User.InvalidCredentials:
        print("Invalid user credentials, please try again.")
        create_superuser()
    sys.exit(0)


@command('assets')
def assets():
    print("Rebuilding assets")
    rebuild_assets()
    sys.exit(0)


def pre_init():
    arg_dict = vars(exts.args)
    for name, value in arg_dict.items():
        try:
            cmd_handler = COMMANDS[name]
        except KeyError:
            pass
        else:
            if value:
                cmd_handler()
