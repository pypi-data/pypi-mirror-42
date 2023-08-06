from flask import g, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def before_request(key, scheme=''):
    serializer = Serializer(key)

    def inner():
        token = request.headers.get('Authorization')

        assert token, '请检查Authorization是否为空'
        assert token[len(scheme)] == scheme, 'scheme不匹配'

        g.auth = serializer.loads(token[len(scheme):])

    return inner


def active(app):
    assert app.config.SECRET_KEY, '请先设置SECRET_KEY'
    app.before_request(before_request(app.config.SECRET_KEY))

    app.logger.info('Active: auth header')
