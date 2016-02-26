import datetime
import uuid

from bottle import request

from .base import DBDataWrapper
from .users import User


class BaseToken(DBDataWrapper):

    class Error(Exception):
        pass

    class KeyNotFound(Error):
        pass

    class KeyExpired(Error):
        pass

    _table = 'confirmations'
    _columns = (
        'key',
        'email',
        'expires',
    )

    @property
    def has_expired(self):
        return self.expires < datetime.datetime.now()

    def delete(self):
        query = self._db.Delete(self._table, where='key = :key')
        self._db.query(query, key=self.key)

    def accept(self):
        raise NotImplementedError()

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @classmethod
    def create(cls, email, expiration, db=None):
        db = db or request.db.sessions
        key = cls.generate_key()
        expires = (datetime.datetime.utcnow() +
                   datetime.timedelta(days=expiration))
        data = {'key': key,
                'email': email,
                'expires': expires}
        query = db.Insert(cls._table, cols=cls._columns)
        db.execute(query, data)
        return cls(data, db=db)

    @classmethod
    def get(cls, key, db=None):
        db = db or request.db.sessions
        query = db.Select(sets=cls._table, where='key = :key')
        db.execute(query, dict(key=key))
        data = db.result
        if not data:
            raise cls.KeyNotFound()

        confirmation = cls(data, db=db)
        if confirmation.has_expired:
            confirmation.delete()
            raise cls.KeyExpired()

        return confirmation


class EmailVerification(BaseToken):

    def accept(self):
        user = User.get(self.email)
        user.confirm().make_logged_in()
        self.delete()
        return user


class PasswordReset(BaseToken):

    def accept(self, new_password):
        user = User.get(self.email)
        user.set_password(new_password)
        self.delete()
        return user

