import sys

from . import Command
from ..app.exts import container as exts


class InviteHook(object):
    def __init__(self, email, netloc):
        self.email = email
        self.netloc = netloc

    def __call__(self):
        # This import has to be made here because the database container is not
        # a lazy object, and therefore causes the class instantiation to break
        # when imported at the top.
        from ..models.auth import InvitationToken
        token = InvitationToken.new(self.email)
        token_path = exts.app.get_url('auth:accept_invitation', key=token.key)
        if self.netloc:
            print(self.netloc + token_path)
            sys.exit(0)
        host = exts.config['server.bind']
        port = exts.config['server.port']
        print('http://{}:{}{}'.format(host, port, token_path))
        sys.exit(0)


class Invite(Command):
    name = 'invite'
    help = 'add invitation token and print its URL'

    def add_args(self):
        self.group.add_argument('email', metavar='EMAIL', help='recipient '
                                'email')
        self.group.add_argument('--netloc', metavar='URL',
                                help='netloc that should be prefixed to '
                                'the token path in http://foo format '
                                '(defaults to server parameters in the '
                                'configuration file)')

    def run(self, args):
        email = args.email
        netloc = args.netloc
        self.exts.add_hook('pre_start', InviteHook(email, netloc))
