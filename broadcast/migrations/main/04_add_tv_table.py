SQL = """
create table tv
(
    id varchar primary_key unique not null,
    created timestamp not null,         -- timestamp when tv object was created
    email varchar,                      -- email of user who created the object
    name varchar,                       -- username of user who created the object
    file_path varchar,                  -- file path relative to upload root
    file_size integer,                  -- file size in bytes
    title varchar,                      -- tv title chosen by user
    license varchar,                    -- tv license chosen by user
    language varchar,                   -- tv language chosen by user
    charge_id varchar,                  -- stripe charge object id, if set tv has priority
    notified timestamp,                 -- time when notification about this item was sent
    status varchar                      -- status representing current state of request
);
"""


def up(db, conf):
    db.executescript(SQL)
