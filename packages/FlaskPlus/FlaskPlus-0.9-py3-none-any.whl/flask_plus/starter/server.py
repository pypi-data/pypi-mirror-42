import multiprocessing

from gunicorn.app.base import BaseApplication

from flask_plus.starter.util import Starter


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


class ServerStarter(Starter):
    def start(self):
        if len(self.modules) == 1:
            # 如果modules只有一个，则直接运行在/路由下
            self.app.register_module(self.modules[0].as_posix())
        else:
            # 如果modules有多个，则分别运行在/path路由下
            for module, path in zip(self.modules, self.paths):
                self.app.register_module(module.as_posix(), prefix=path)

        options = {
            'bind': '0.0.0.0:80',
            'workers': multiprocessing.cpu_count(),
        }

        Application(self.app, options).run()


def run():
    ServerStarter().run()
