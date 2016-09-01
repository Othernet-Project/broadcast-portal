import datetime
import json


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        super(DateTimeDecoder, self).__init__(object_hook=self.object_hook,
                                              *args,
                                              **kargs)

    def object_hook(self, obj):
        if '__type__' not in obj:
            return obj

        obj_type = obj.pop('__type__')
        try:
            return datetime(**obj)
        except Exception:
            obj['__type__'] = obj_type
            return obj


def jsonify(obj):
    return json.dumps(obj, cls=DateTimeEncoder)


def dejsonify(s):
    return json.loads(s, cls=DateTimeDecoder)


def jsonify_file(obj, fd):
    json.dump(obj, fd, cls=DateTimeEncoder, sort_keys=True, indent=4,
              separators=(',', ':'))


def dejsonify_file(fd):
    return json.load(fd, cls=DateTimeDecoder)
