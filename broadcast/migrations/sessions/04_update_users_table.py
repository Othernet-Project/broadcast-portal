SQL = """
alter table users rename to tmp;
create table users
(
    username varchar unique,                        -- username
    password varchar,                               -- encrypted password
    is_superuser boolean not null default 0,        -- is admin user
    created timestamp not null,                     -- user creation timestamp
    email varchar primary_key unique not null,      -- email address
    confirmed timestamp,                            -- email confirmed timestamp
    options varchar default '{}'                    -- arbitary user data
);
replace into users
(username, password, is_superuser, created, email, confirmed, options)
select
username, password, is_superuser, created, email, confirmed, options
from tmp;
drop table tmp;
"""


def up(db, conf):
    db.executescript(SQL)

