import datetime
import sqlite3
import uuid

from ..app.exts import container as exts
from . import Model


class Bin(Model):
    dbname = 'main'
    table = 'bins'
    columns = (
        'id',
        'created',
        'closed',
        'capacity',
        'size',
        'count',
    )
    pk = 'id'

    class NotEnoughSpace(Model.Error):
        """
        Exception raised when bin's maximum capacity is already reached.
        """
        pass

    def can_accept(self, item):
        """
        Return whether the :py:class:`Bin` instance has enough free space to
        store the passed in ``item`` or not.
        """
        return self.size + item.size <= self.capacity

    def add(self, item):
        """
        Add the passed in ``item`` to the bin.
        """
        if self.closed:
            raise RuntimeError("Cannot add files to a closed bin")

        if not self.can_accept(item):
            raise self.NotEnoughSpace()

        try:
            self.update(size=self.size + item.size,
                        count=self.count + 1)
        except sqlite3.IntegrityError:
            raise self.NotEnoughSpace()
        else:
            item.update(bin=self.id)

    def remove(self, item):
        """
        Remove the passed in ``item`` from the bin.
        """
        if item.bin != self.id:
            raise RuntimeError("Cannot remove file from bin as"
                               " it's not part of it")
        self.update(size=self.size - item.size,
                    count=self.count - 1)
        item.update(bin=None)

    def close(self):
        """
        Mark the bin as closed by writing the current timestamp to the closed
        column.
        """
        self.update(closed=datetime.datetime.utcnow())

    @classmethod
    def new(cls, cursor=None, config=None):
        """
        Create a new empty bin and return the instance wrapping it.
        """
        config = config or exts.config
        data = {
            'created': datetime.datetime.utcnow(),
            'capacity': config['bin.capacity'],
            'size': 0,
            'count': 0,
        }
        instance = cls(data)
        instance.save(cursor=cursor, pk=uuid.uuid4().hex)
        return instance

    @classmethod
    def current(cls, cursor=None, config=None):
        """
        Return the currently open bin instance, and if there's none open
        create a new one.
        """
        try:
            return cls.get(cursor=cursor, closed=None)
        except Bin.NotFound:
            return cls.new(cursor=cursor, config=config)
