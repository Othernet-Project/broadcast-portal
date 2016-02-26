import random
import string
import urllib
import urlparse


def is_string(obj):
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)


def from_csv(raw_value):
    return [val.strip() for val in (raw_value or '').split(',') if val]


def to_csv(values):
    return ','.join(values)


def row_to_dict(row):
    return dict((key, row[key]) for key in row.keys()) if row else {}


def get_redirect_path(base_path, next_path, next_param_name='next'):
    QUERY_PARAM_IDX = 4

    next_encoded = urllib.urlencode({next_param_name: next_path})

    parsed = urlparse.urlparse(base_path)
    new_path = list(parsed)

    if parsed.query:
        new_path[QUERY_PARAM_IDX] = '&'.join([new_path[QUERY_PARAM_IDX],
                                              next_encoded])
    else:
        new_path[QUERY_PARAM_IDX] = next_encoded

    return urlparse.urlunparse(new_path)


def generate_random_key(letters=True, digits=True, punctuation=True,
                        length=50):
    charset = []
    if letters:
        charset.append(string.ascii_letters)
    if digits:
        charset.append(string.digits)
    if punctuation:
        charset.append(string.punctuation)

    if not charset:
        return ''

    chars = (''.join(charset).replace('\'', '')
                             .replace('"', '')
                             .replace('\\', ''))
    return ''.join([random.choice(chars) for i in range(length)])
