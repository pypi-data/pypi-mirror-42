from types import ModuleType, FunctionType
from datetime import datetime

from flask import Response, current_app
from werkzeug.exceptions import HTTPException
from bson import ObjectId
from ujson import dumps


class Keys:
    def keys(self):
        return [key for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))]

    def __getitem__(self, item):
        return getattr(self, item)


def data_cleaning(rv):
    if rv is None:
        return rv
    if isinstance(rv, (str, int, float)):
        return rv
    if isinstance(rv, bytes):
        return rv.decode()
    if isinstance(rv, ObjectId):
        return str(rv)
    if isinstance(rv, datetime):
        return rv.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(rv, list):
        return [data_cleaning(_) for _ in rv]
    if isinstance(rv, dict):
        return {data_cleaning(k): data_cleaning(v) for k, v in rv.items()}

    # 是否是模块
    if isinstance(rv, ModuleType):
        return data_cleaning({k: v for k, v in rv.__dict__.items() if k.isupper()})

    # 是否是类
    if isinstance(rv, type):
        return data_cleaning(dict(type('mixin', (rv, Keys), {})()))

    # 是否是函数
    if isinstance(rv, FunctionType):
        return data_cleaning(rv())

    # 实例是否有keys和__getitem__属性
    if hasattr(rv, 'keys') and hasattr(rv, '__getitem__'):
        return data_cleaning(dict(rv))

    # 其它实例
    if isinstance(rv, object):
        return data_cleaning(
            {k: getattr(rv, k) for k in dir(rv) if not k.startswith('__') and not callable(getattr(rv, k))})

    return rv


class APIResponse(Response):
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, response, environ=None):
        if not isinstance(response, HTTPException):
            response = current_app.response_class(dumps(data_cleaning(response)) + '\n')
        return super(Response, cls).force_type(response, environ)
