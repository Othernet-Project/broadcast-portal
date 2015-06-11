SQL = """
alter table users add column email varchar unique not null;
alter table users add column is_verified boolean not null default 0;
"""


def up(db, config):
    db.executescript(SQL)
