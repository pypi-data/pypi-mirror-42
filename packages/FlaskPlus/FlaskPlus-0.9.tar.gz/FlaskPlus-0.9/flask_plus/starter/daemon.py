import importlib.util

from flask_plus.starter.util import Starter


class DaemonStarter(Starter):
    def start(self):
        if len(self.modules) == 1:
            importlib.import_module(self.modules[0].as_posix()).run()
        else:
            from concurrent.futures import ProcessPoolExecutor

            pool = ProcessPoolExecutor(len(self.modules))
            for module in self.modules:
                pool.submit(importlib.import_module(module.as_posix()).run)
            pool.wait()


def run():
    DaemonStarter().run()
