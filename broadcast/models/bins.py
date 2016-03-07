import datetime
import sqlite3

from bottle import request

from ..util.basemodel import Model


class Bin(Model):

    class NotEnoughSpace(Model.Error):
        pass

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    ARCHIVED = 'ARCHIVED'

    database = 'main'
    table = 'bins'
    columns = (
        'id',
        'created',
        'closes',
        'capacity',
        'size',
        'count',
        'status',
    )
    pk_field = 'id'

    @property
    def usage(self):
        try:
            return self.size * 100.0 / self.capacity
        except ZeroDivisionError:
            return 0

    @property
    def time_left(self):
        return self.closes - datetime.datetime.utcnow()

    def can_accept(self, item):
        return self.size + item.size <= self.capacity

    def add(self, item):
        if not self.can_accept(item):
            raise self.NotEnoughSpace()

        try:
            self.update(size=self.size + item.size,
                        count=self.count + 1)
        except sqlite3.IntegrityError:
            raise self.NotEnoughSpace()
        else:
            item.update(bin=self.id, status=item.ACCEPTED)
            return self

    def remove(self, item):
        self.update(size=self.size - item.size,
                    count=self.count - 1)
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
        db = db or cls.get_database()
        config = config or request.app.config
        query = db.Select(sets=cls.table,
                          where='status = :status',
                          order='-created',
                          limit=1)
        db.query(query, status=cls.OPEN)
        raw_data = db.result
        if not raw_data:
            return cls.new(db=db, config=config)
        # check if bin lifetime already exceeded the limit
        if datetime.datetime.utcnow() >= raw_data['closes']:
            # if so, close older bin(s), and return a newly created one
            new_bin = cls.new(db=db, config=config)
            where = 'status = :old_status AND id != :exclude_id'
            query = db.Update(cls.table,
                              where=where,
                              status=':new_status')
            db.query(query,
                     old_status=cls.OPEN,
                     new_status=cls.CLOSED,
                     exclude_id=new_bin.id)
            return new_bin
        return cls(raw_data, db=db)

    @classmethod
    def new(cls, db=None, config=None):
        db = db or cls.get_database()
        config = config or request.app.config
        created = datetime.datetime.utcnow()
        closes = created + datetime.timedelta(seconds=config['bin.lifetime'])
        data = {'id': cls.generate_unique_id(),
                'created': created,
                'closes': closes,
                'capacity': config['bin.capacity'],
                'size': 0,
                'status': cls.OPEN}
        return cls.create(db=db, **data)

