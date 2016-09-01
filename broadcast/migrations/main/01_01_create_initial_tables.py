SQL = """
create table bins
(
    id text primary key unique,
    created timestamp,          -- creation timestamp
    closed timestamp,           -- finalization timestamp
    capacity integer not null,  -- maximum allowed size (bytes)
    size integer default 0,     -- total size (bytes)
    count integer default 0,    -- number of items in the bin
    check (size <= capacity)    -- constraint to ensure size never exceeds capacity
);

create table content
(
    id text primary key unique,
    created timestamp,          -- creation timestamp
    email text,                 -- creator email
    username text,              -- creator username
    ipaddr text,                -- creator IP address
    path text,                  -- file path relative to upload root
    size integer default 0,     -- file size in bytes
    bin text,                   -- bin ID
    votes integer default 0,    -- number of votes
    category text               -- category name
);

create table votes
(
    id integer primary key,
    created timestamp,          -- time when vote was cast
    username text,              -- voter's username
    ipaddr text,                -- voter's IP address
    value integer,              -- vote value (usually +1, 0, or -1)
    content_id text,            -- content
    constraint uidcid unique (username, content_id) on conflict replace
);
"""


def up(db, conf):
    db.executescript(SQL)
