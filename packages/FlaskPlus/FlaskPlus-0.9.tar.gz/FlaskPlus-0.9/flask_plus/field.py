from contextlib import suppress
from functools import wraps

from bson import ObjectId
from flask import request


def parse(func):
    @wraps(func)
    def _wrapper(self, key='id', nullable=False):
        ret = None
        with suppress(Exception):
            if isinstance(self.target, dict) and key in self.target:
                ret = func(self, self.target[key])
            elif isinstance(self.target, list):
                ret = func(self, self.target)

        assert nullable or ret is not None, 'No valid value found in "{}"'.format(key)
        return ret

    return _wrapper


class Field:
    @property
    def target(self):
        raise NotImplementedError


class Args(Field):
    @property
    def target(self):
        return request.args

    @parse
    def objid(self, data):
        return ObjectId(data) if ObjectId.is_valid(data) else None

    @parse
    def objids(self, data):
        return list(map(ObjectId, filter(ObjectId.is_valid, data.split(','))))

    @parse
    def int(self, data):
        return int(data) if str.isdigit(data) else None

    @parse
    def ints(self, data):
        return list(map(int, filter(str.isdigit, data.split(','))))

    @parse
    def float(self, data):
        return float(data) if data.replace('.', '', 1).isdigit() else None

    @parse
    def floats(self, data):
        return list(map(float, filter(lambda v: v.replace('.', '', 1).isdigit(), data.split(','))))

    @parse
    def str(self, data):
        return data if data else None

    @parse
    def strs(self, data):
        return list(filter(lambda v: v, data.split(',')))

    @parse
    def bool(self, data):
        return {'true': True, 'false': False}.get(data.lower(), None)


class Json(Field):

    @property
    def target(self):
        return request.json

    @parse
    def objid(self, data):
        return ObjectId(data) if isinstance(data, str) and ObjectId.is_valid(data) else None

    @parse
    def objids(self, data):
        return list(map(ObjectId, filter(ObjectId.is_valid, data))) if isinstance(data, list) else None

    @parse
    def int(self, data):
        return data if isinstance(data, int) else None

    @parse
    def ints(self, data):
        return list(filter(lambda v: isinstance(v, int), data)) if isinstance(data, list) else None

    @parse
    def float(self, data):
        return data if isinstance(data, (int, float)) else None

    @parse
    def floats(self, data):
        return list(filter(lambda v: isinstance(v, (int, float)), data)) if isinstance(data, list) else None

    @parse
    def str(self, data):
        return data if isinstance(data, str) and len(data) > 0 else None

    @parse
    def strs(self, data):
        return list(filter(lambda v: isinstance(v, str) and len(v) > 0, data)) if isinstance(data, list) else None

    @parse
    def list(self, data):
        return data if isinstance(data, list) else None

    @parse
    def lists(self, data):
        return list(filter(lambda v: isinstance(v, list), data)) if isinstance(data, list) else None

    @parse
    def dict(self, data):
        return data if isinstance(data, dict) else None

    @parse
    def dicts(self, data):
        return list(filter(lambda v: isinstance(v, dict), data)) if isinstance(data, list) else None

    @parse
    def bool(self, data):
        return data if isinstance(data, bool) else None


class Obj(Json):

    def __init__(self, target):
        self.__target = target

    @property
    def target(self):
        return self.__target


args = Args()
json = Json()
obj = Obj
