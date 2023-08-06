from flask_plus import exts


def active(app):
    assert app.config.CONFIG_URL, '请先设置CONFIG_URL'
    assert not hasattr(exts, 'config'), '变量cofnig已被挂载'

    app.config.from_remote(app.config.CONFIG_URL)

    exts.config = app.config
    app.logger.info('Active: remote_config')
