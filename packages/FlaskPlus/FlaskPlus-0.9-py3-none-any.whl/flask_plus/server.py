import importlib.util
import multiprocessing
import os
import re
import sys
from pathlib import Path

from gunicorn.app.base import BaseApplication
from gunicorn.util import getcwd

from flask_plus import FlaskPlus

# 有顺序要求
EXTS = [
    'remote_config',
    'mongo_logging',
    'file_logging',
    'kong_header',
    'auth_header',
    'mongo',
    'redis',
    'minio_storage',
    'minio_hash_storage'
]

# 一般使用文件名作为path即可，不用特别指定；
# 有时如token想做为path但是不能作为文件名的时候，则文件别名，指定path为token
rules = {
    'ext': str.split,
    'path': str.strip
}

m_content = re.compile('"""(.+?)"""', re.S)
m_kv = re.compile('@(\S+)\s([^@]*)')


def convert(kv_):
    kv = {}
    for k, v in kv_:
        if k in rules:
            kv[k] = rules[k](v)
    return kv


class Application(BaseApplication):
    def __init__(self, app, options):
        self.application = app
        self.options = options
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application


def load_module(file):
    spec = importlib.util.spec_from_file_location(file.stem, file.as_posix())
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def create_app():
    assert len(sys.argv) > 1, '请指定运行的文件'

    modules = [Path(_) for _ in sys.argv[1:]]
    for module in modules:
        if not module.is_file():
            raise ModuleNotFoundError('Modules {} 不存在'.format(module.as_posix()))

    exts = []
    paths = []
    for module in modules:
        content = m_content.match(module.read_text())
        if content:
            kv = convert(m_kv.findall(content.group(1)))

            if kv.get('ext'):
                exts.extend(kv['ext'])

            if kv.get('path'):
                paths.append(kv['path'])
            else:
                paths.append(module.stem)

    exts = set(exts)

    app = FlaskPlus(__name__)

    for e in EXTS:
        if e in exts:
            ext = importlib.import_module('flask_plus.ext.{}'.format(e))
            ext.active(app)
            exts.remove(e)

    if exts:
        raise ModuleNotFoundError('Extensions {} 不存在'.format(' '.join(exts)))

    if len(modules) == 1:
        # 如果modules只有一个，则直接运行在/路由下
        app.register_module(modules[0].as_posix())
    else:
        # 如果modules有多个，则分别运行在/path路由下
        for module, path in zip(modules, paths):
            app.register_module(module.as_posix(), prefix=path)

    return app


def main():
    cwd = getcwd()
    os.chdir(cwd)
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    options = {
        'bind': '0.0.0.0:80',
        'workers': multiprocessing.cpu_count(),
    }

    Application(create_app(), options).run()
