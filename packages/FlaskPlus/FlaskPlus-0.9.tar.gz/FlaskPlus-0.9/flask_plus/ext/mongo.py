from pymongo import MongoClient

from flask_plus import exts


def active(app):
    assert app.config.MONGO_URL, '请先设置MONGO_URL'
    assert not hasattr(exts, 'mongo'), '变量mongo已被挂载'

    url, db = app.config.MONGO_URL.rsplit('/', 1)
    exts.mongo = MongoClient(url)[db]
    app.logger.info('Active: pymongo')
