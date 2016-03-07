SQL = """
create table bins
(
    id varchar primary_key unique not null,
    created timestamp not null,
    closes timestamp not null,
    capacity integer not null,
    size integer not null default 0,
    count integer not null default 0,
    status varchar not null,
    check (size <= capacity)
);
"""


def up(db, conf):
    db.executescript(SQL)

