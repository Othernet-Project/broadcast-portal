SQL = """
create table content
(
    content_id varchar primary_key unique not null,
    email varchar not null,
    name varchar not null,
    file_path varchar not null,         -- file path relative to upload root
    file_size integer not null,
    title varchar not null,
    license varchar not null,
    url varchar not null,
    created timestamp not null,         -- timestamp when content object was created
    charge_id varchar,                  -- stripe charge object id, if set content has priority
    charged_at timestamp,               -- timestamp of funds reservation
    captured_at timestamp               -- timestamp when funds actually arrived
);
"""


def up(db, conf):
    db.executescript(SQL)
