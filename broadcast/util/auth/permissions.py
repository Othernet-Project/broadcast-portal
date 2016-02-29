import functools
import json

from bottle import request

from .base import DateTimeDecoder, DateTimeEncoder
from .utils import is_string


class BasePermission(object):
    name = None  # subclasses should provide a unique identifier

    def __init__(self, *args, **kwargs):
        if self.name is None:
            raise ValueError("Permisson class has no `name` attribute "
                             "specified.")

    def is_granted(self, *args, **kwargs):
        """The default behavior is that solely a permission object's presence
        in a group grants access. However, if special conditions need to be
        checked, subclasses may override this method and perform custom
        verifications."""
        return True

    @classmethod
    def subclasses(cls, source=None):
        """Recursively collect all subclasses of ``cls``, not just direct
        descendants.

        :param source:  On subsequent recursive calls, source will point to a
                        child class that needs to be inspected.
        """
        source = source or cls
        result = source.__subclasses__()
        for child in result:
            result.extend(cls.subclasses(source=child))
        return result

    @classmethod
    def cast(cls, name):
        for subclass in cls.subclasses():
            if subclass.name == name:
                return subclass

        raise ValueError("No Permission class found under the name: "
                         "{0}".format(name))


class BaseDynamicPermission(BasePermission):

    def __init__(self, identifier, db):
        super(BaseDynamicPermission, self).__init__()
        self.db = db or request.db.sessions
        self.identifier = identifier
        self.data = self._load()

    def _load(self):
        q = self.db.Select(
            sets='permissions',
            where='name = :name AND identifier = :identifier'
        )
        self.db.query(q, name=self.name, identifier=self.identifier)
        result = self.db.result
        if result:
            return json.loads(result['data'], cls=DateTimeDecoder)
        return {}

    def save(self):
        q = self.db.Replace('permissions',
                            constraints=('name', 'identifier'),
                            cols=('name', 'identifier', 'data'))
        data = json.dumps(self.data, cls=DateTimeEncoder)
        self.db.query(q,
                      name=self.name,
                      identifier=self.identifier,
                      data=data)


class ACLPermission(BaseDynamicPermission):
    name = 'acl'

    NO_PERMISSION = 0
    READ = 4
    WRITE = 2
    EXECUTE = 1
    ALIASES = {
        'r': READ,
        'w': WRITE,
        'x': EXECUTE,
        READ: READ,
        WRITE: WRITE,
        EXECUTE: EXECUTE
    }
    VALID_BITMASKS = range(1, 8)

    def to_bitmask(func):
        @functools.wraps(func)
        def wrapper(self, path, permission):
            if is_string(permission):
                try:
                    bitmask = sum([self.ALIASES[p] for p in list(permission)])
                except KeyError:
                    msg = "Invalid permission: {0}".format(permission)
                    raise ValueError(msg)
            else:
                bitmask = permission

            if bitmask not in self.VALID_BITMASKS:
                msg = "Invalid permission: {0}".format(permission)
                raise ValueError(msg)

            return func(self, path, bitmask)
        return wrapper

    @to_bitmask
    def grant(self, path, permission):
        existing = self.data.get(path, self.NO_PERMISSION)
        self.data[path] = existing | permission
        self.save()

    @to_bitmask
    def revoke(self, path, permission):
        existing = self.data.get(path, self.NO_PERMISSION)
        permission = existing & ~permission
        if permission == self.NO_PERMISSION:
            # when having no permission, we can freely just remove the whole
            # path as not having a path at all also means having no permissions
            # whatsoever
            self.data.pop(path, None)
        else:
            self.data[path] = permission

        self.save()

    def clear(self):
        self.data = {}
        self.save()

    @to_bitmask
    def is_granted(self, path, permission):
        existing = self.data.get(path, self.NO_PERMISSION)
        return existing & permission == permission
