SQL = """
create table content
(
    id varchar primary_key unique not null,
    created timestamp not null,         -- timestamp when content object was created
    email varchar,                      -- email of user who created the object
    name varchar,                       -- username of user who created the object
    file_path varchar,                  -- file path relative to upload root
    file_size integer,                  -- file size in bytes
    title varchar,                      -- content title chosen by user
    license varchar,                    -- content license chosen by user
    language varchar,                   -- content language chosen by user
    url varchar,                        -- content url chosen by user
    charge_id varchar,                  -- stripe charge object id, if set content has priority
    notified timestamp,                 -- time when notification about this item was sent
    status varchar                      -- status representing current state of request
);
"""


def up(db, conf):
    db.executescript(SQL)
