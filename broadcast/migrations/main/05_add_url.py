SQL = """
alter table content add column url varchar;
"""


def up(db, conf):
    db.executescript(SQL)

