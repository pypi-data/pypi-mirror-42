import logging
import os

from flask_plus import exts


def active(app):
    assert not hasattr(exts, 'log'), '变量log已被挂载'

    if app.config.LOGGING_NAME:
        app.logger.name = app.config.LOGGING_NAME

    if app.config.LOGGING_LEVEL:
        app.logger.setLevel(app.config.LOGGING_LEVEL)

    handler = logging.FileHandler(
        filename=app.config.LOGGING_FILE or os.path.join(app.root_path, 'log.txt'))
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    app.logger.addHandler(handler)

    exts.log = app.logger

    app.logger.info('Active: file logging')
