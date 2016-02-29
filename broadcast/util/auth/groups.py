from bottle import request

from .permissions import BasePermission
from .utils import from_csv, row_to_dict


class BaseGroup(object):
    """Subclasses should provide functionality for storing group objects in the
    chosen storage backend."""
    def __init__(self, name, permissions=None, has_superpowers=False):
        """
        :param name:             string - unique group name
        :param permissions:      list of permission names that will be used to
                                 find their respective classes
        :param has_superpowers:  bool, if set, all permissions are granted
        """
        self.name = name
        self.has_superpowers = has_superpowers
        # assemble list of permission classes
        permissions = permissions or []
        self.permission_classes = [BasePermission.cast(perm)
                                   for perm in permissions]

    def contains_permission(self, permission_class):
        return permission_class in self.permission_classes

    def add_permission(self, permission_class):
        self.permission_classes.append(permission_class)

    def remove_permission(self, permission_class):
        if self.contains_permission(permission_class):
            self.permission_classes.remove(permission_class)

    @property
    def permissions(self):
        return [cls.name for cls in self.permission_classes]


class Group(BaseGroup):

    class GroupNotFound(Exception):
        pass

    def __init__(self, db, *args, **kwargs):
        self.db = db or request.db.sessions
        super(Group, self).__init__(*args, **kwargs)

    @classmethod
    def from_name(cls, group_name, db):
        db = db or request.db.sessions
        query = db.Select(sets='groups', where='name = :name')
        db.query(query, name=group_name)
        group = db.result
        group = row_to_dict(group) if group else {}

        if group:
            group['permissions'] = from_csv(group.pop('permissions', ''))
            return cls(db=db, **group)

        raise cls.GroupNotFound(group_name)

    def save(self):
        query = self.db.Replace(
            'groups',
            constraints=['name'],
            cols=('name', 'permissions', 'has_superpowers'),
        )
        self.db.query(query,
                      name=self.name,
                      permissions=self.permissions,
                      has_superpowers=self.has_superpowers)
