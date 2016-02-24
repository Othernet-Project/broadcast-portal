SQL = """
alter table content add column bin varchar;
"""


def up(db, conf):
    db.executescript(SQL)

