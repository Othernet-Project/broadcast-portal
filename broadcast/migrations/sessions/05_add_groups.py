SQL = """
create table groups
(
    name varchar primary_key,                       -- unique group name
    permissions text,                               -- comma separated list of permissions
    has_superpowers boolean not null default 0      -- is superuser?
);
"""

SQL_CREATE_GROUP = """
INSERT INTO groups (name, permissions, has_superpowers)
VALUES ('superuser', '', 1);
INSERT INTO groups (name, permissions, has_superpowers)
VALUES ('moderator', '', 0);
"""


def up(db, conf):
    db.executescript(SQL)
    # create needed groups
    db.executescript(SQL_CREATE_GROUP)
