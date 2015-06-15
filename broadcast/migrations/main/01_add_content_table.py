SQL = """
create table content
(
    content_id varchar primary_key unique not null,
    email varchar not null,
    name varchar not null,
    file_path varchar not null,         -- file path relative to upload root
    title varchar not null,
    license varchar not null,
    url varchar not null,
    created timestamp not null,
    is_priority boolean not null default 0
);
"""


def up(db, conf):
    db.executescript(SQL)
