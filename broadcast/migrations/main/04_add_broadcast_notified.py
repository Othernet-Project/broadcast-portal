SQL = """
alter table content add column notified timestamp;
alter table twitter add column notified timestamp;
"""


def up(db, conf):
    db.executescript(SQL)
