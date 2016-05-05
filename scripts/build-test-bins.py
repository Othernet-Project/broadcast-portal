import os
import random
import datetime
from itertools import repeat

from sqlize import Insert


BIN_TABLE = 'bins'
FILE_TABLE = 'content'
OUTFILE = 'test-queries.sql'

RANDOMCHARS = 'abcdef0123456789'
BASETIME = datetime.datetime(2016, 5, 5, 12, 0, 0)
ID_LEN = 32
HOUR = 3600
DAY = HOUR * 24
WEEK = DAY * 7


def random_ts():
    delta = random.randrange(-WEEK, DAY, 1)
    return BASETIME + datetime.timedelta(seconds=delta)


def random_path_component():
    return ''.join(random.choice(RANDOMCHARS) for i in range(10))


def random_content_file():
    random_segment = '/'.join(
        random_path_component() for i in range(random.randrange(1, 5)))
    path = os.path.join('/tmp/content-testing/', random_segment, 'test.file')
    return path


def random_string(len):
    """
    Random string
    """
    return ''.join(random.choice(RANDOMCHARS) for i in range(len))


def generate_query(table, data):
    columns = [col for col in data]
    values = ["'{}'".format(data[col]) for col in data]
    query = Insert(table, cols=columns, vals=values)
    return query


def random_file(bin):
    """
    Factory for random files datapoints. The returned data has the following
    attributes:
    - ``id`` (unique primary key for the file)
    - ``bin`` (bin the file belongs to)
    - ``url`` (URL the path was obtained from, optional)
    - ``path`` (path the file can be found at)
    - ``size`` (size of the file)
    - ``email`` (email of the user who submitted the file)
    - ``title`` (title of the file, optional)
    - ``status`` (whether the file was accepted or not, values include
    - ``created`` (date the file was created at)
    - ``license`` (license the file was published under, optional)
    - ``language`` (language the content is in, optional)
    - ``notified`` (date notifications went out for this file, may be null)
    """
    return {
        'id': random_string(ID_LEN),
        'bin': bin,
        'url': '',
        'path': random_content_file(),
        'size': '1',
        'email': 'tester@outernet.is',
        'title': 'test-' + random_string(10),
        'status': 'ACCEPTED',
        'created': random_ts().strftime("%Y-%m-%d %H:%M:%S.%f"),
        'license': '',
        'language': '',
        'notified': '',
    }


def random_bin():
    """
    Factory for random daily bin datapints. The returned data has the following
    attributes:
        - ``id`` (unique primary key for the bins, ex.
                  38ab0ea1d7a3485d97efd8bb2e50490b)
        - ``size`` (size used by the bin)
        - ``count`` (number of files in the bin)
        - ``status`` (could be OPEN or CLOSED)
        - ``closes`` (the time the bin was closed (24h after created))
        - ``created`` (the time the bin was created so files could be added)
        - ``capacity`` (total size available)
    """
    bin_id = random_string(ID_LEN)
    count = random.randrange(2, 20, 1)
    created_timestamp = random_ts()
    closes_timestamp = created_timestamp + datetime.timedelta(seconds=DAY)
    return {
        'id': bin_id,
        'size': str(count),
        'count': str(count),
        'status': "CLOSED",
        'closes': closes_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
        'created': created_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
        'capacity': str(4000),
    }


def generate_query_list():
    bin = random_bin()
    id = bin['id']
    count = int(bin['count'])
    queries = [generate_query(BIN_TABLE, bin)]
    for _ in repeat(None, count):
        # hand file queries second because bin is a foreign key
        queries.append(generate_query(FILE_TABLE, random_file(id)))
    return queries


def main():
    queries = []
    for _ in repeat(None, random.randrange(10, 30, 1)):
        queries += generate_query_list()
    textblob = '\n'.join([str(q) for q in queries])
    with open(OUTFILE, 'w') as out:
        out.write(textblob)
    print('you can find the generated queries in: {}'.format(OUTFILE))


if __name__ == "__main__":
    main()
