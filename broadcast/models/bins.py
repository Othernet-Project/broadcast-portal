import uuid
import datetime

from . import Model


class Bin(Model):
    dbname = 'main'
    table = 'bins'
    columns = (
        'id',
        'created',
        'closed',
        'size',
        'count',
    )
    pk = 'id'

    def add(self, item):
        if self.closed:
            raise RuntimeError('Cannot add files to a closed bin')
        self.size += item.size
        self.count += 1
        item.bin = self.id

    def close(self):
        self.closed = datetime.datetime.utcnow()
        self.save()

    @classmethod
    def new(cls, config=None):
        data = {
            'created': datetime.datetime.utcnow(),
            'size': 0,
            'count': 0,
        }
        bin = cls(data)
        bin.save(pk=uuid.uuid4().hex)
        return bin
