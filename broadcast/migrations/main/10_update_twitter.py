SQL = """
alter table twitter rename to tmp;
create table twitter
(
    id varchar primary_key unique not null,
    created timestamp not null,
    email varchar,
    handle varchar,
    notified timestamp,
    status varchar
);
replace into twitter
(id, created, email, handle, notified, status)
select
id, created, email, handle, notified, status
from tmp;
drop table tmp;
"""


def up(db, conf):
    db.executescript(SQL)


