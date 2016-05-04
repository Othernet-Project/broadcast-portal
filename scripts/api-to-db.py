import os
import json
import sqlite3
from datetime import datetime
from contextlib import contextmanager

import requests
import confloader
from sqlize import Insert


def submit_request(url, user, password):
    print('connecting to {}'.format(url))
    res = requests.get(url, auth=(user, password))
    assert res.ok
    return res.content


def get_latest_bin_id(api_path, user, password):
    response = submit_request(api_path + 'bins/', user, password)
    results = json.loads(response)['results']
    results = sorted(results, lambda x, y: cmp(x['closes'], y['closes']))
    for bin in results:
        if bin['status'] == "OPEN":
            continue
        return bin


def get_file_list(bin_id, api_path, user, password):
    response = submit_request(
        api_path + 'bins/{}/items/'.format(bin_id), user, password)
    results = json.loads(response)['results']
    return results


@contextmanager
def yield_database(f):
    conn = sqlite3.connect(f)
    c = conn.cursor()
    submit_query(c,
                 '''
                    CREATE TABLE IF NOT EXISTS actions
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datestamp DATE NOT NULL,
                        action TEXT NOT NULL,
                        path TEXT NOT NULL,
                        serve_path TEXT NOT NULL
                    );
                 ''')
    yield c
    conn.commit()
    conn.close()


def submit_query(c, query, data=None):
    """ Submits the query, handling optional data
    Designed to open and close the database in a single op
    """
    if data:
        c.execute(query, data)
    else:
        c.execute(query)


def write_record(action, path, serve_path, cursor):
    """ Writes the record for a performed action """
    data = {
        'datestamp': datetime.now(),
        'action': action,
        'path': path,
        'serve_path': serve_path
    }
    query = Insert('actions', cols=data.keys())
    submit_query(cursor, str(query), data)


def main():
    confpath = confloader.get_config_path(default='config.ini')
    conf = confloader.ConfDict.from_file(confpath, defaults={
        'db-file': 'community-bin.db',
        'user': 'asdf',
        'pass': 'asdf',
        'api-path': 'http://localhost:8080/api/',
        'upload-dir': 'Community Uploads'
    })
    user = conf['user']
    password = conf['pass']
    api_path = conf['api-path']
    bin = get_latest_bin_id(api_path, user, password)
    files = get_file_list(bin['id'], api_path, user, password)
    with yield_database(conf['db-file']) as cursor:
        for f in files:
            path = f['path']
            serve_path = os.path.join(
                conf['upload-dir'], os.path.basename(f['path']))
            write_record('sent', path, serve_path, cursor)


if __name__ == "__main__":
    main()
