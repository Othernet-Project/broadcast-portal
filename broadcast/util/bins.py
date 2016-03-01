import datetime
import sqlite3
import uuid

from bottle import request


class Bin(object):

    class Error(Exception):
        pass

    class NotEnoughSpace(Error):
        pass

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    ARCHIVED = 'ARCHIVED'

    _table = 'bins'
    _columns = (
        'id',
        'created',
        'closes',
        'capacity',
        'size',
        'status',
    )
    _pk_field = 'id'

    def __init__(self, data, db=None):
        self._db = db or request.db.main
        # in case a dict-like object is passed in
        if not isinstance(data, dict):
            data = dict((k, data[k]) for k in data.keys())

        self._data = data

    def __getattr__(self, name):
        if name in self._columns:
            return self._data.get(name, None)
        raise AttributeError(name)

    @property
    def usage(self):
        try:
            return self.size * 100 / self.capacity
        except ZeroDivisionError:
            return 0

    @property
    def time_left(self):
        return self.closes - datetime.datetime.utcnow()

    def update(self, **kwargs):
        if any([key not in self._columns for key in kwargs]):
            raise ValueError("Unknown columns detected.")

        placeholders = dict((name, ':{}'.format(name))
                            for name in kwargs.keys())
        where = '{pk_field} = :{pk_field}'.format(pk_field=self._pk_field)
        query = self._db.Update(self._table,
                                where=where,
                                **placeholders)
        query_args = dict(kwargs)
        query_args[self._pk_field] = getattr(self, self._pk_field)
        self._db.query(query, **query_args)
        self._data.update(kwargs)
        return self

    def can_accept(self, item):
        return self.size + item.size <= self.capacity

    def add(self, item):
        if not self.can_accept(item):
            raise self.NotEnoughSpace()

        try:
            self.update(size=self.size + item.size)
        except sqlite3.IntegrityError:
            raise self.NotEnoughSpace()
        else:
            item.update(bin=self.id, status=item.ACCEPTED)
            return self

    def remove(self, item):
        self.update(size=self.size - item.size)
        item.update(bin=None, status=item.REJECTED)
        return self

    def close(self):
        self.update(status=self.CLOSED)
        return self

    def archive(self):
        self.update(status=self.ARCHIVED)
        return self

    @classmethod
    def current(cls, db=None, config=None):
        db = db or request.db.main
        config = config or request.app.config
        query = db.Select(sets=cls._table,
                          where='status = :status',
                          order='-created',
                          limit=1)
        db.query(query, status=cls.OPEN)
        raw_data = db.result
        if not raw_data:
            return cls.create(db=db, config=config)
        # check if bin lifetime already exceeded the limit
        if datetime.datetime.utcnow() >= raw_data['closes']:
            # if so, close older bin(s), and return a newly created one
            new_bin = cls.create(db=db, config=config)
            where = 'status = :old_status AND id != :exclude_id'
            query = db.Update(cls._table,
                              where=where,
                              status=':new_status')
            db.query(query,
                     old_status=cls.OPEN,
                     new_status=cls.CLOSED,
                     exclude_id=new_bin.id)
            return new_bin
        return cls(raw_data, db=db)

    @classmethod
    def create(cls, db=None, config=None):
        db = db or request.db.sessions
        config = config or request.app.config
        created = datetime.datetime.utcnow()
        closes = created + datetime.timedelta(seconds=config['bin.lifetime'])
        data = {'id': cls.get_unique_id(),
                'created': created,
                'closes': closes,
                'capacity': config['bin.capacity'],
                'size': 0,
                'status': cls.OPEN}
        query = db.Insert(cls._table, cols=cls._columns)
        db.execute(query, data)
        return cls(data, db=db)

    @staticmethod
    def get_unique_id():
        return uuid.uuid4().hex

