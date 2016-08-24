SQL = """
create table bins
(
    id varchar primary_key unique,
    created timestamp,      -- creation timestamp
    closed timestamp,       -- finalization timestamp
    size integer,           -- total size (bytes)
    count integer           -- number of items in the bin
);

create table content
(
    id varchar primary_key unique,
    created timestamp,      -- creation timestamp
    email varchar,          -- creator email
    username varchar,       -- creator username
    ipaddr varchar,         -- creator IP address
    path varchar,           -- file path relative to upload root
    size integer,           -- file size in bytes
    bin varchar,            -- bin ID
    votes integer,          -- number of votes
    category varchar        -- category name
);

create table votes
(
    id integer primary_key,
    created timestamp,                  -- time when vote was cast
    name varchar,                       -- voter's username
    is_upvote varchar,                  -- whether vote is an upvote
    content_id integer                  -- content
);
"""


def up(db, conf):
    db.executescript(SQL)
