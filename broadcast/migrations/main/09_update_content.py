SQL = """
alter table content rename to tmp;
create table content
(
    id varchar primary_key unique not null,
    created timestamp not null,
    email varchar,
    path varchar,
    size integer,
    title varchar,
    license varchar,
    language varchar,
    notified timestamp,
    status varchar,
    url varchar,
    bin varchar
);
replace into content
(id, created, email, path, size, title, license, language, notified, status)
select
id, created, email, file_path, file_size, title, license, language, notified, status
from tmp;
drop table tmp;
"""


def up(db, conf):
    db.executescript(SQL)

