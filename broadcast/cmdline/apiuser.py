import uuid

import pbkdf2

from . import Command
from ..util.serializers import jsonify_file, dejsonify_file


class ApiUser(Command):
    name = 'apiuser'
    help = 'create or update an API user account'

    def add_args(self):
        self.group.add_argument('apiuser', metavar='NAME',
                                help='API user name')

    @staticmethod
    def get_acl(acl_file):
        try:
            with open(acl_file, 'r') as f:
                return dejsonify_file(f)
        except Exception:
            return {}

    @staticmethod
    def save_acl(acl_file, data):
        with open(acl_file, 'w') as f:
            jsonify_file(data, f)

    def run(self, args):
        acl_file = self.exts.config['app.api_acl']
        username = args.apiuser
        password = uuid.uuid4().hex
        acl = self.get_acl(acl_file)
        acl[username] = pbkdf2.crypt(password)
        self.save_acl(acl_file, acl)
        print('Acccess token for {}: {}'.format(username, password))
        print('{} updated'.format(acl_file))
        self.quit(0)
