from redis import StrictRedis

from flask_plus import exts


def active(app):
    assert app.config.REDIS_URL, '请先设置REDIS_URL'
    assert not hasattr(exts, 'redis'), '变量redis已被挂载'

    exts.redis = StrictRedis.from_url(app.config.REDIS_URL, decode_responses=True)
    app.logger.info('Active: redis')
