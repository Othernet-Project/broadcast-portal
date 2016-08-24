SQL = """
create table users
(
    id integer primary_key,     -- user ID
    email text unique,          -- email address
    username text unique,       -- username
    password text,              -- encrypted password
    created timestamp,          -- user creation timestamp
    confirmed timestamp,        -- email confirmed timestamp
    data text default '{}',     -- arbitary user data
    groupname text              -- comma separated list of groups
);

create table tokens
(
    key text unique primary_key,    -- token ID
    email text,                     -- target email
    expires timestamp,              -- expiry timestamp
);

create table sessions
(
    session_id text primary_key unique,     -- session id
    data text,                              -- arbitary session data
    expires timestamp not null              -- timestamp when session expires
);
"""


def up(db, conf):
    db.executescript(SQL)