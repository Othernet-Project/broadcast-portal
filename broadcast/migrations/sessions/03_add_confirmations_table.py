SQL = """
create table confirmations
(
    key varchar primary_key unique not null,   -- confirmation key
    email varchar not null,                    -- email address
    created timestamp not null                 -- confirmation created timestamp
);
"""


def up(db, conf):
    db.executescript(SQL)
