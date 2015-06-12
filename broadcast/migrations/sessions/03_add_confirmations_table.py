SQL = """
create table confirmations
(
    key varchar primary_key unique not null,   -- confirmation key
    email varchar not null,                    -- email address
    expires timestamp not null                 -- confirmation expires timestamp
);
"""


def up(db, conf):
    db.executescript(SQL)
