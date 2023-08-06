from flask import g, request


def before_request():
    g.custom_id = request.headers.get('X-Consumer-Custom-Id')
    g.username = request.headers.get('X-Consumer-Username')

    assert g.custom_id, '请检查X-Consumer-Custom-Id是否为空'
    assert g.username, '请检查X-Consumer-Username是否为空'


def active(app):
    app.before_request(before_request)

    app.logger.info('Active: kong header')
