import uuid

from . import Model
from .items import ContentItem
from ..util.helpers import utcnow


class Bin(Model):
    dbname = 'main'
    table = 'bins'
    columns = (
        'id',
        'created',
        'size',
        'count',
    )
    pk = 'id'

    @property
    def items(self):
        q = self.db.Select(sets=ContentItem.table,
                           order=['-votes', '-created'],
                           where='bin = :bin')
        return ContentItem.iter(self.db.query(q, bin=self.id))

    @classmethod
    def list(cls):
        q = cls.db.Select(sets=cls.table,
                          what=['id', 'created'],
                          order='-created')
        for row in cls.db.query(q):
            yield cls(row)

    @classmethod
    def last(cls):
        q = cls.db.Select(sets=cls.table,
                          order='-created',
                          limit=1)
        result = cls.db.query(q).result
        if not result:
            raise cls.NotFound()
        return cls(result)

    @classmethod
    def new(cls):
        bin_id = uuid.uuid4().hex
        count, size = ContentItem.finalize_candidates(bin_id)
        if not count:
            return None
        data = {
            'created': utcnow(),
            'size': size,
            'count': count,
        }
        bin = cls(data)
        bin.save(pk=bin_id)
        return bin
