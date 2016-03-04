SQL = """
alter table charges rename to tmp;
create table charges
(
    id varchar unique,                       -- stripe charge object id
    charged_at timestamp,                    -- timestamp of funds reservation
    captured_at timestamp,                   -- timestamp when funds actually arrived
    plan varchar,                            -- payment plan, also determines whether charge_id is a subscription or fixed payment
    item_id varchar,                         -- id of item to which the charge object belongs
    item_type varchar                        -- type of item to which the charge object belons
);
replace into charges
(id, charged_at, captured_at)
select
id, charged_at, captured_at
from tmp;
drop table tmp;
update charges
set item_id = (select content.id from content where content.charge_id = charges.id),
    item_type = 'content'
where id in (select charge_id from content where charge_id is not null);
update charges
set item_id = (select twitter.id from twitter where twitter.charge_id = charges.id),
    plan = (select twitter.plan from twitter where twitter.charge_id = charges.id),
    item_type = 'twitter'
where id in (select charge_id from twitter where charge_id is not null);
"""


def up(db, conf):
    db.executescript(SQL)

