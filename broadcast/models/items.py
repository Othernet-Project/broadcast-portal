import os
import uuid
import datetime
from contextlib import contextmanager

import pytz
from squery_lite.squery import Cursor

from ..util.helpers import to_timestamp
from ..app.exts import container as exts
from ..util.helpers import utcnow
from . import Model


class IsCandidate(object):
    """
    Custom SQL function that determines whether an item is a bin candidate
    """
    def __init__(self):
        self.limit = exts.config['bin.capacity']
        self.total = 0

    def __call__(self, size, votes):
        if votes < 1:
            return 0
        self.total += size
        return self.total <= self.limit


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
        'username',
        'value',
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

    def save_file(self, file_object, cid):
        upload_root = exts.config['content.upload_root']
        # make sure folder with id exists
        upload_dir = os.path.join(upload_root, cid)
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
        cid = uuid.uuid4().hex
        item.save_file(file_object, cid)
        item.save(pk=cid)

    def cast_vote(self, username, is_upvote, ipaddr):
        """
        Cast a vote by specified user for this item. This method creates a new
        Vote item, persists it into the database, and updates the vote count.

        During vote-casting, an exlusive lock is held on the database to
        prevent miscalculation of the vote count.

        Votes can be -1, 0, or +1. User can always change between these three
        values, but they can't go beyond the -1 and +1 limit. When upvoting is
        done on a value of +1, then the value remains +1 and nothing happens.
        If downvoting is done on a value of -1, then, again, nothing happens.
        Whether voting was done or not, affects the return value. If no voting
        was recorded, ``None`` is returned by this method. Otherwise a
        timestamp is returned.
        """
        now = utcnow()
        vote_value = 1 if is_upvote else -1

        try:
            vote = Vote.get(username=username, content_id=self.id)
        except Vote.NotFound:
            vote = Vote({
                'content_id': self.id,
                'created': now,
                'username': username,
                'value': vote_value,
                'ipaddr': ipaddr,
            })
        else:
            if vote.value == vote_value:
                return
            vote.value += vote_value
        finally:
            vote.save()

        # FIXME: Perhaps we need a better way than holding an exclusive lock
        # here because this can become a bottleneck.
        with self.db.transaction(new_connection=True, exclusive=True) as cur:
            # Existing record is updated, so we have the latest vote count
            self.reload(cur)
            self.votes += vote_value
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
    @contextmanager
    def candidate_query_cursor(cls):
        conn = cls.db.connection.new()
        conn.add_func(IsCandidate())
        yield Cursor(conn)
        conn.close()

    @classmethod
    def candidate_stats(cls):
        q = cls.db.Select(
            'sum(size) as size, count(*) as count',
            sets=cls.table,
            where=['bin ISNULL', 'iscandidate(size, votes) = 1'],
            order=['-votes', '-created'])
        with cls.candidate_query_cursor() as cursor:
            return cursor.query(q).result

    @classmethod
    def binless_items(cls, limit=None, offset=None, kind=None, username=None):
        """
        Generator of items that are not yet in a bin
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

        if username:
            # If username is passed, then join the contents table to a subqury
            # filtering votes that were cast by the specified username, and
            # return a sum of vote values (therefore -1, 0 or +1) as
            # 'user_vote' column for each record.
            subq = cls.db.Select(['votes.content_id', 'votes.value'],
                                 sets='votes',
                                 where='votes.username = :username')
            q.what.append('sum(user_votes.value) as user_vote')
            q.sets.join(subq.as_subquery() + ' as user_votes',
                        kind=cls.db.LEFT,
                        on='user_votes.content_id = content.id')
            q.group = 'content.id'

        with cls.candidate_query_cursor() as cursor:
            for row in cursor.query(q, username=username).results:
                yield cls(row)

    @classmethod
    def last_activity(cls):
        ts_vote = Vote.last_update()
        ts_item = cls.last_update()
        return max([ts_vote, ts_item])
