import os
import uuid
import datetime

import pytz

from ..util.helpers import to_timestamp
from ..app.exts import container as exts
from ..util.helpers import utcnow
from . import Model


class LastUpdateMixin(object):
    VERY_OLD = datetime.datetime(1, 1, 1, tzinfo=pytz.utc)

    @classmethod
    def last_update(cls):
        q = cls.db.Select(['created'], sets=cls.table, order=['-created'],
                          limit=1)
        try:
            return cls.db.query(q).result.created
        except AttributeError:
            return cls.VERY_OLD


class Vote(Model, LastUpdateMixin):
    dbname = 'main'
    table = 'votes'
    columns = (
        'id',
        'created',
        'name',
        'is_upvote',
        'content_id',
        'ipaddr',
    )


class ContentItem(Model, LastUpdateMixin):
    dbname = 'main'
    database = 'main'
    table = 'content'
    columns = (
        'id',
        'created',
        'email',
        'username',
        'ipaddr',
        'path',
        'size',
        'bin',
        'votes',
        'category',
    )

    Vote = Vote

    ALL = 0
    CANDIDATES = 1
    NON_CANDIDATES = 2

    @property
    def filename(self):
        return os.path.basename(self.path)

    def save_file(self, file_object):
        upload_root = exts.config['content.upload_root']
        # make sure folder with id exists
        upload_dir = os.path.join(upload_root, self.id)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        upload_path = os.path.join(upload_dir, file_object.filename)
        if os.path.exists(upload_path):
            # remove file if already exists
            os.remove(upload_path)

        file_object.save(upload_path)
        self.path = os.path.relpath(upload_path, upload_root)
        self.size = os.stat(upload_path).st_size

    @classmethod
    def new(cls, email, username, ipaddr, file_object, category=None):
        data = {
            'created': utcnow(),
            'email': email,
            'username': username,
            'ipaddr': ipaddr,
            'category': category,
        }
        item = cls(data)
        item.attach_file(file_object)
        item.save(pk=uuid.uuid4().hex)

    def cast_vote(self, username, is_upvote, ipaddr):
        """
        Cast a vote by specified user for this item. This method creates a new
        Vote item, persists it into the database, and updates the vote count.

        During vote-casting, an exlusive lock is held on the database to
        prevent miscalculation of the vote count.
        """
        # TODO: Perhaps we need a better way than holding an exclusive lock
        # here because this can become a bottleneck.
        now = utcnow()
        with self.db.transaction(new_connection=True, exclusive=True) as cur:
            # Existing record is updated, so we have the latest vote count
            self.reload(cur)
            vote = Vote({
                'contentid': self.id,
                'created': now,
                'name': username,
                'is_upvote': is_upvote,
                'ipaddr': ipaddr,
            })
            vote.save(cur)
            if is_upvote:
                self.votes += 1
            else:
                self.votes -= 1
            self.save(cur)
        exts.last_update['timestamp'] = to_timestamp(now)
        return now

    @classmethod
    def search_binless(cls, term):
        """
        Generator of items that match given term and
        """
        q = cls.db.Select(sets=cls.table,
                          where=['bin ISNULL', 'ilike(title, %:term%) = 1'],
                          order=['-votes', '-created'])
        for row in cls.db.query(q, term=term):
            yield cls(row)

    @classmethod
    def candidate_stats(cls):
        q = cls.db.Select(
            'sum(size) as size, count(*) as count',
            sets=cls.table,
            where=['bin ISNULL', 'iscandidate(size, votes) = 1'],
            order=['-votes', '-created'])
        return cls.db.query(q).result

    @classmethod
    def binless_items(cls, limit=None, offset=None, kind=None):
        """
        Generator of items that are not yet in a bin

        .. warning::
            This generator opens a database transaction which is *not* closed
            until the iteration is complete. The caller must ensure the
            iteration is done to the end to prevent memory leak.
        """
        what = list(cls.columns)
        what.append('iscandidate(size, votes) as is_candidate')
        q = cls.db.Select(what, sets=cls.table, where=['bin ISNULL'],
                          order=['-votes', '-created'], limit=limit,
                          offset=offset)
        if kind == cls.CANDIDATES:
            q.where &= 'iscandidate(size, votes) = 1'
        elif kind == cls.NON_CANDIDATES:
            q.where &= 'iscandidate(size, votes) = 0'
        for row in cls.db.query(q).results:
            yield cls(row)

    @classmethod
    def last_activity(cls):
        ts_vote = Vote.last_update()
        ts_item = cls.last_update()
        return max([ts_vote, ts_item])
