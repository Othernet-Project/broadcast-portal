SQL = """
alter table users rename to tmp;
create table users
(
    username varchar unique,                        -- username
    password varchar,                               -- encrypted password
    created timestamp not null,                     -- user creation timestamp
    email varchar primary_key unique not null,      -- email address
    confirmed timestamp,                            -- email confirmed timestamp
    data varchar default '{}',                      -- arbitary user data
    groups text                                     -- comma separated list of groups
);
replace into users
(username, password, created, email, confirmed, data)
select
username, password, created, email, confirmed, options
from tmp;
drop table tmp;
"""


def up(db, conf):
    db.executescript(SQL)

