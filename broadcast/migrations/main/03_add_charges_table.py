SQL = """
create table charges
(
    id varchar primary_key unique not null,  -- stripe charge object id
    charged_at timestamp not null,           -- timestamp of funds reservation
    captured_at timestamp                    -- timestamp when funds actually arrived
);
"""


def up(db, conf):
    db.executescript(SQL)
