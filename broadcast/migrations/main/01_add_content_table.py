SQL = """
create table content
(
    id varchar primary_key unique not null,
    created timestamp not null,         -- timestamp when content object was created
    email varchar not null,             -- email of user who created the object
    name varchar not null,              -- username of user who created the object
    file_path varchar not null,         -- file path relative to upload root
    file_size integer not null,         -- file size in bytes
    title varchar not null,             -- content title chosen by user
    license varchar not null,           -- content license chosen by user
    url varchar not null,               -- content url chosen by user
    charge_id varchar                   -- stripe charge object id, if set content has priority
);
"""


def up(db, conf):
    db.executescript(SQL)
