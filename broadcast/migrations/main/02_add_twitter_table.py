SQL = """
create table twitter
(
    id varchar primary_key unique not null,
    email varchar not null,
    name varchar not null,
    handle varchar not null,            -- twitter handle
    plan varchar not null,              -- payment plan
    created timestamp not null,         -- timestamp when content object was created
    charge_id varchar,                  -- stripe charge object id, if set content has priority
    charged_at timestamp,               -- timestamp of funds reservation
    captured_at timestamp               -- timestamp when funds actually arrived
);
"""


def up(db, conf):
    db.executescript(SQL)
