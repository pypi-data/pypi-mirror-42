from flask import current_app, request
from werkzeug.exceptions import HTTPException


def error(err):
    current_app.logger.warning('Error', exc_info=True)
    return {'err': str(err)}, 400


def http_error(err):
    current_app.logger.warning('{} {} {}'.format(request.method, request.full_path, err.code))
    return {'err': err.name}, 400


def exception(err):
    current_app.logger.exception('Exception')
    return {'err': 'Exception'}, 400


def exp_handler(app):
    app.register_error_handler(AssertionError, error)
    app.register_error_handler(HTTPException, http_error)
    app.register_error_handler(Exception, exception)
