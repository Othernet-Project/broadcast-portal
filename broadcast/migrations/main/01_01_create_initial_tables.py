SQL = """
create table bins
(
    id text primary_key unique,
    created timestamp,      -- creation timestamp
    closed timestamp,       -- finalization timestamp
    size integer default 0, -- total size (bytes)
    count integer default 0 -- number of items in the bin
);

create table content
(
    id text primary_key unique,
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
    id integer primary_key,
    created timestamp,          -- time when vote was cast
    username text,              -- voter's username
    ipaddr text,                -- voter's IP address
    is_upvote integer,          -- whether vote is an upvote
    content_id integer          -- content
);
"""


def up(db, conf):
    db.executescript(SQL)
