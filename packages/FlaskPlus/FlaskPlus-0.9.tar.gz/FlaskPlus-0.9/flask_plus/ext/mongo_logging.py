import logging
import traceback

from pymongo import MongoClient

from flask_plus import exts


class MongoHandler(logging.Handler):
    def __init__(self, uri):
        super().__init__()
        self.db = self.mongo_init(uri)

    def emit(self, record):
        self.db.log.insert_one({
            'time': record.created,
            'name': record.name,
            'levelname': record.levelname,
            'msg': record.msg,
            'exception': traceback.format_exception(*record.exc_info) if record.exc_info else None
        })

    @staticmethod
    def mongo_init(uri):
        url, db = uri.rsplit('/', 1)
        return MongoClient(url)[db]


def active(app):
    assert app.config.LOGGING_URL, '请先设置LOGGING_URL'
    assert not hasattr(exts, 'log'), '变量log已被挂载'

    if app.config.LOGGING_NAME:
        app.logger.name = app.config.LOGGING_NAME

    if app.config.LOGGING_LEVEL:
        app.logger.setLevel(app.config.LOGGING_LEVEL)

    app.logger.addHandler(MongoHandler(app.config.LOGGING_URL))

    exts.log = app.logger

    app.logger.info('Active: mongo logging')
