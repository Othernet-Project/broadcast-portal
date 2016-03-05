import json
import uuid

from bottle import request

from .serializers import DateTimeEncoder, DateTimeDecoder


class Model(object):
    _command_delimiter = '__'

    database = None
    table = None
    columns = None
    order = None

    class Error(Exception):
        pass

    class DoesNotExist(Error):
        pass

    def __init__(self, data=None, db=None):
        self._db = db or self.get_database()
        data = data or dict()
        # data must be json-serializable, make sure it is
        if not isinstance(data, dict):
            data = dict((k, data[k]) for k in data.keys())

        self._data = data

    def __getattr__(self, name):
        if name in self.columns:
            return self._data.get(name, None)
        raise AttributeError(name)

    def to_native(self):
        return dict(self._data)

    def to_json(self):
        return json.dumps(self._data, cls=DateTimeEncoder)

    def update(self, **kwargs):
        if any([key not in self.columns for key in kwargs]):
            raise ValueError("Unknown columns detected.")

        placeholders = dict((name, ':{}'.format(name))
                            for name in kwargs.keys())
        where = '{pk_field} = :{pk_field}'.format(pk_field=self.pk_field)
        query = self._db.Update(self.table,
                                where=where,
                                **placeholders)
        query_args = dict(kwargs)
        query_args[self.pk_field] = getattr(self, self.pk_field)
        self._db.query(query, **query_args)
        self._data.update(kwargs)
        return self

    @classmethod
    def from_json(cls, data, db=None):
        return cls(json.loads(data, cls=DateTimeDecoder), db=db)

    @classmethod
    def get_database(cls):
        return request.db[cls.database]

    @classmethod
    def _unpack_command(cls, command, value):
        splitted = command.split(cls._command_delimiter)
        if len(splitted) > 1:
            (field, op) = splitted
            if op.lower() == 'like':
                value = '%{value}%'.format(value=value)

            return (field, op, value)

        (field,) = splitted
        return (field, 'IS' if value is None else '=', value)

    @classmethod
    def _construct_query(cls, db, **kwargs):
        query = db.Select(sets=cls.table)
        if cls.order:
            query.order += cls.order

        params = dict()
        for (command, value) in kwargs.items():
            (field, operator, value) = cls._unpack_command(command, value)
            params[field] = value
            query.where += '{field} {op} :{field}'.format(field=field,
                                                          op=operator)
        return (query, params)

    @classmethod
    def get(cls, db=None, **kwargs):
        db = db or cls.get_database()
        (query, params) = cls._construct_query(db=db, **kwargs)
        db.query(query, **params)
        raw_data = db.result
        if not raw_data:
            raise cls.DoesNotExist()

        return cls(raw_data, db=db)

    @classmethod
    def filter(cls, db=None, **kwargs):
        db = db or cls.get_database()
        (query, params) = cls._construct_query(db=db, **kwargs)
        db.query(query, **params)
        return [cls(raw_data, db=db) for raw_data in db.results]

    @classmethod
    def create(cls, db=None, **kwargs):
        db = db or cls.get_database()
        writable_columns = [col for col in kwargs if col in cls.columns]
        query = db.Insert(cls.table, cols=writable_columns)
        db.execute(query, kwargs)
        return cls(kwargs, db=db)

    @staticmethod
    def generate_unique_id():
        return uuid.uuid4().hex

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
    def cast(cls, into):
        for subclass in cls.subclasses():
            if subclass.table == into:
                return subclass

        raise TypeError("Unable to cast into: {}".format(into))

