from __future__ import print_function

import sys

from . import Command


try:
    raw_input
except NameError:
    raw_input = input


GROUPS = ['user', 'moderator', 'superuser']


class AdduserHook(object):
    def __init__(self, username, email, password, group, overwrite=False,
                 confirmed=False):
        self.username = username
        self.email = email
        self.password = password
        self.group = group
        self.overwrite = overwrite
        self.confirmed = confirmed

    def __call__(self):
        # This import has to be made here because the database container is not
        # a lazy object, and therefore causes the class instantiation to break
        # when imported at the top.
        from ..models.auth import User

        try:
            user = User.new(username=self.username, email=self.email,
                            password=self.password, group=self.group,
                            overwrite=self.overwrite, confirmed=self.confirmed)
        except User.IntegrityError:
            print('ERROR: Username or email taken', file=sys.stderr)
            sys.exit(1)
        else:
            print('User account created')
            print('record ID: {}'.format(user.id))
            print('username:  {}'.format(user.username))
            print('email:     {}'.format(user.email))
            print('group:     {}'.format(user.group))
            sys.exit(0)


class Adduser(Command):
    name = 'adduser'
    help = 'add an user account'

    def add_args(self):
        self.group.add_argument('username', metavar='USERNAME', help='name of '
                                'the user account')
        self.group.add_argument('email', metavar='EMAIL', help='email address '
                                'of the account')
        self.group.add_argument('password', metavar='PASSWORD', help='clear '
                                'text password to use with the new user')
        self.group.add_argument('--groupname', metavar='GROUP',
                                choices=GROUPS, help='make user member of '
                                'this group', default='user')
        self.group.add_argument('--super', action='store_true',
                                help='make user a superuser (redundant with '
                                '--groupname)')
        self.group.add_argument('--overwrite', action='store_true',
                                help='replace users with the same email or '
                                'username')
        self.group.add_argument('--confirmed', action='store_true',
                                help='mark account as confirmed')

    def run(self, args):
        if args.super:
            group = 'superuser'
        else:
            group = args.groupname
        hook = AdduserHook(username=args.username, email=args.email,
                           password=args.password, group=group,
                           overwrite=args.overwrite, confirmed=args.confirmed)
        self.exts.add_hook('pre_start', hook)
