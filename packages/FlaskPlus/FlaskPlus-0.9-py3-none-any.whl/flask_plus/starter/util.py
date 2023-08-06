import importlib
import os
import re
import sys
from copy import deepcopy
from pathlib import Path

from flask_plus import FlaskPlus


class Starter:
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

    def __init__(self):
        self.app = FlaskPlus(__name__)
        self.modules = []
        self.exts = []
        self.paths = []

    def convert(self, kv_):
        kv = {}
        for k, v in kv_:
            if k in self.rules:
                kv[k] = self.rules[k](v)
        return kv

    @staticmethod
    def getcwd():
        # get current path, try to use PWD env first
        try:
            a = os.stat(os.environ['PWD'])
            b = os.stat(os.getcwd())
            if a.st_ino == b.st_ino and a.st_dev == b.st_dev:
                cwd = os.environ['PWD']
            else:
                cwd = os.getcwd()
        except:
            cwd = os.getcwd()
        return cwd

    def chdir(self):
        cwd = self.getcwd()
        os.chdir(cwd)
        if cwd not in sys.path:
            sys.path.insert(0, cwd)

    def run(self):
        assert len(sys.argv) > 1, '请指定运行的文件'
        self.chdir()

        modules = [Path(_) for _ in sys.argv[1:]]
        for module in modules:
            if not module.is_file():
                raise ModuleNotFoundError('Modules {} 不存在'.format(module.as_posix()))

        for module in modules:
            content = self.m_content.match(module.read_text())
            if content:
                kv = self.convert(self.m_kv.findall(content.group(1)))

                if kv.get('ext'):
                    self.exts.extend(kv['ext'])

                if kv.get('path'):
                    self.paths.append(kv['path'])
                else:
                    self.paths.append(module.stem)

        self.exts = list(set(self.exts))
        exts = deepcopy(self.exts)

        for e in self.EXTS:
            if e in exts:
                ext = importlib.import_module('flask_plus.ext.{}'.format(e))
                ext.active(self.app)
                exts.remove(e)

        if exts:
            raise ModuleNotFoundError('Extensions {} 不存在'.format(' '.join(exts)))

        self.start()

    def start(self):
        raise NotImplementedError('请在子类中实现启动方式')
