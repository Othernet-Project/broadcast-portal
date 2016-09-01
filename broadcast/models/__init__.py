import sqlite3

from ..app.exts import container as exts
from ..util.serializers import jsonify, dejsonify


def to_list(names):
    return ', '.join(names)


def to_key(name):
    return ':{}'.format(name)


def to_keys(names):
    return to_list(map(to_key, names))


def to_set_args(names):
    return {n: to_key(n) for n in names}


def to_equals(name):
    return '{0} = :{0}'.format(name)


class ModelMeta(type):
    def __init__(cls, name, bases, dct):
        if cls.dbname:
            cls.db = exts.db[cls.dbname]
        super(ModelMeta, cls).__init__(name, bases, dct)


class Model(object):
    __metaclass__ = ModelMeta

    dbname = None
    table = None
    columns = {}
    extra_columns = {}
    pk = 'id'

    # Alias sqlite3 error classes for easy access
    Error = sqlite3.Error
    DataError = sqlite3.DataError
    DatabaseError = sqlite3.DatabaseError
    IntegrityError = sqlite3.IntegrityError
    InterfaceError = sqlite3.InterfaceError
    NotSupportedError = sqlite3.NotSupportedError
    OperationalError = sqlite3.OperationalError
    ProgrammingError = sqlite3.ProgrammingError

    class ModelError(Exception):
        pass

    class LookupError(Exception):
        pass

    class NotFound(LookupError):
        pass

    class Gone(LookupError):
        pass

    def __init__(self, data):
        self.set_data(data)

    def set_data(self, data):
        data = data or dict()
        if not isinstance(data, dict):
            # Data is not an instance of a dict, so it's probably a row from
            # the sqlite3 row factory. We need to make sure it's a proper dict
            # so it can be JSON-serialized
            data = dict((k, data[k]) for k in data.keys())
        self._data = {}
        self._extras = {}
        self.extra_columns = []
        for k, v in data.items():
            if k in self.columns:
                self._data[k] = v
            else:
                self._extras[k] = v
                self.extra_columns.append(k)

    def get_pk(self):
        """
        Returns the primary key of the record.
        """
        return self._data.get(self.pk)

    def reload(self, cursor=None):
        """
        Reload the data for the current object from the database. The record is
        looked up based on the primary key column value.
        """
        q = self.db.Select(sets=self.table, where=[self.where_pk()], limit=1)
        if not cursor:
            cursor = self.db.cursor()
        result = cursor.query(q, pk=self.get_pk()).result
        if not result:
            raise self.Gone('The record matching this object no longer exists')
        self.set_data(result)

    def update(self, cursor=None, **kwargs):
        """
        Update the data of the current object, first in the database, and if no
        exception was raised, on the object instance itself as well.
        """
        if any([key not in self.columns for key in kwargs]):
            raise ValueError("Unknown columns detected.")

        placeholders = dict((name, ':{}'.format(name))
                            for name in kwargs.keys())
        where = '{pk_field} = :{pk_field}'.format(pk_field=self.pk)
        query = self.db.Update(self.table,
                               where=where,
                               **placeholders)
        query_args = dict(kwargs)
        query_args[self.pk] = getattr(self, self.pk)
        cursor = cursor or self.db.cursor()
        cursor.query(query, **query_args)
        # as an exception wasn't raised, it's safe to update the instance data
        self.set_data(kwargs)

    def delete(self, cursor=None):
        """
        DELETEs the record matching the current object's primary key
        """
        q = self.db.Delete(self.table, where=self.where_pk())
        cursor = cursor or self.db.cursor()
        cursor.query(q, pk=self.get_pk())

    def save(self, cursor=None, pk=None, force_replace=False):
        """
        Performs an INSERT or REPLACE. REPLACE is performed only when the
        current objet has a pk or ``force_replace`` argument is ``True``. If
        ``pk`` argument is specified, the object's primary key will be set to
        the specified value just before executing the query. The value is
        ignored if the object already has a primary key. If the primary key
        value is not specified, it is assumed that the database will set it
        automatically (e.g., ``INTEGER PIRMARY KEY`` column).

        It is not checked whether the matching record was deleted meanwhile,
        however, REPLACE always succeeds switching behavior to INSERT if no
        matching record is found. It is therefore the caller's responsibility
        to perform any necessary checks to ensure the record will not be
        restored by accident.
        """
        if self.get_pk() or force_replace:
            qrycls = self.db.Replace
        else:
            qrycls = self.db.Insert
            if pk:
                self._data[self.pk] = pk
        cursor = cursor or self.db.cursor()
        q = qrycls(self.table, cols=self._data.keys())
        cursor.query(q, **self._data)
        return cursor

    def to_json(self):
        data = self._data.copy()
        data.update(self._extras)
        return jsonify(data)

    @classmethod
    def from_json(cls, data):
        return cls(dejsonify(data))

    @classmethod
    def where_pk(cls):
        """
        Returns a WHERE expression for the pk. The key name for the pk is
        always 'pk' regardless of the actual column name.
        """
        return '{} = :pk'.format(cls.pk)

    @classmethod
    def iter(cls, cursor):
        """
        Generator that iterates over a cursor and returns instances of the
        ``Model`` object for each row.
        """
        for row in cursor:
            yield cls(row)

    @classmethod
    def get(cls, pk=None, cursor=None, **lookup):
        """
        Get a single record from the database that matches the specified
        primary key. If pk is omitted, but keyword arguments are passed, a
        record matching the specified keyword arguments will be looked up. The
        keywords arguments are expected to be in ``column_name = value``
        format. Keyword arguments are ignored if ``pk`` is passed. If no
        arguments are passed, ``TypeError`` is raised.

        If no matching record is found, ``NotFound`` exception is raised.
        """
        cursor = cursor or cls.db.cursor()
        if not pk and not lookup:
            raise TypeError('Missing pk or keyword arguments')
        if pk:
            where = cls.where_pk()
            kwargs = {'pk': pk}
        else:
            where = ['{0} = :{0}'.format(k) for k in lookup.keys()]
            kwargs = lookup
        q = cls.db.Select(sets=cls.table, where=where, limit=1)
        result = cursor.query(q, **kwargs).result
        if not result:
            raise cls.NotFound('No results with specified query')
        return cls(result)

    def __getattr__(self, name):
        if name in self.columns:
            return self._data.get(name, None)
        if name in self.extra_columns:
            return self._extras.get(name, None)
        raise AttributeError('{} has no attribute {}'.format(self, name))

    def __setattr__(self, name, value):
        if name in self.columns:
            self._data[name] = value
        if name in self.extra_columns:
            self._extras[name] = value
        else:
            object.__setattr__(self, name, value)
