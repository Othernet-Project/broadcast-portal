import datetime
import json

from bottle import request


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        super(DateTimeDecoder, self).__init__(object_hook=self.object_hook,
                                              *args,
                                              **kargs)

    def object_hook(self, obj):
        if '__type__' not in obj:
            return obj

        obj_type = obj.pop('__type__')
        try:
            return datetime(**obj)
        except Exception:
            obj['__type__'] = obj_type
            return obj


class DBDataWrapper(object):

    def __init__(self, data=None, db=None):
        self._db = db or request.db.sessions
        # if user logs out, an empty user object is needed
        if not data:
            data = dict((k, None) for k in self._columns)
        # data must be json-serializable, make sure it is
        if not isinstance(data, dict):
            data = dict((k, data[k]) for k in data.keys())

        self._data = data

    def __getattr__(self, name):
        if name in self._columns:
            return self._data.get(name, None)
        raise AttributeError(name)

    def to_json(self):
        return json.dumps(self._data, cls=DateTimeEncoder)

    @classmethod
    def from_json(cls, data, db=None):
        return cls(json.loads(data, cls=DateTimeDecoder), db=db)

