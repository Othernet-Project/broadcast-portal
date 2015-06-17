SQL = """
create table twitter
(
    id varchar primary_key unique not null,
    created timestamp not null,         -- timestamp when content object was created
    email varchar not null,             -- email of user who created the object
    name varchar not null,              -- username of user who created the object
    handle varchar not null,            -- twitter handle
    plan varchar not null,              -- payment plan, also determines whether charge_id is a subscription or fixed payment
    charge_id varchar                   -- stripe charge or subscription object id, if set content has priority
);
"""


def up(db, conf):
    db.executescript(SQL)
