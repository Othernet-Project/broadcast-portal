import datetime
import uuid

from ..basemodel import Model
from .users import User


class BaseToken(Model):

    class KeyExpired(Model.Error):
        pass

    database = 'sessions'
    table = 'confirmations'
    columns = (
        'key',
        'email',
        'expires',
    )
    pk_field = 'key'

    def __init__(self, *args, **kwargs):
        super(BaseToken, self).__init__(*args, **kwargs)
        if self.has_expired:
            self.delete()
            raise self.KeyExpired()

    @property
    def has_expired(self):
        return self.expires < datetime.datetime.now()

    def delete(self):
        query = self._db.Delete(self.table, where='key = :key')
        self._db.query(query, key=self.key)

    def accept(self):
        raise NotImplementedError()

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @classmethod
    def new(cls, email, expiration, db=None):
        db = db or cls.get_database()
        key = cls.generate_key()
        expires = (datetime.datetime.utcnow() +
                   datetime.timedelta(days=expiration))
        return cls.create(key=key, email=email, expires=expires, db=db)


class EmailVerification(BaseToken):

    def accept(self):
        user = User.get(email=self.email)
        user.confirm().make_logged_in()
        self.delete()
        return user


class PasswordReset(BaseToken):

    def accept(self, new_password):
        user = User.get(email=self.email)
        user.set_password(new_password)
        self.delete()
        return user
