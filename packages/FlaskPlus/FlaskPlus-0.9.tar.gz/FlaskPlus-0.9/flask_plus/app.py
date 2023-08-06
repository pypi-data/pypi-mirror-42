import secrets

from flask import Blueprint, Flask

from .parse import module_parse
from .response import APIResponse
from .config import Config
from .exception import exp_handler


class FlaskPlus(Flask):
    config_class = Config
    response_class = APIResponse

    def __init__(self, *args, **kwargs):
        remove_static = {
            'static_folder': None,
            'template_folder': None
        }
        remove_static.update(kwargs)
        super().__init__(*args, **remove_static)

        exp_handler(self)

    def make_response(self, rv):
        if isinstance(rv, tuple):
            rv = list(rv)
            if rv[0] is None:
                rv[0] = {}
            rv = tuple(rv)
        elif rv is None:
            rv = {}

        return super().make_response(rv)

    def register_module(self, module, prefix=None):
        if prefix:
            prefix = '/' + prefix.replace('__', '/').strip('/')

        bp = Blueprint(secrets.token_hex(8), '')

        routes, before = module_parse(module)
        for route in routes:
            self.logger.info(
                'Route: {} {}'.format(
                    route['methods'][0],
                    (prefix if prefix else '/') if route['rule'] == '/' else (
                                (prefix if prefix else '') + route['rule']))
            )
            bp.add_url_rule(**route, strict_slashes=False)

        if before:
            bp.before_request(before)

        self.register_blueprint(bp, url_prefix=prefix)

    def register_modules(self, module_prefix: dict):
        for module, prefix in module_prefix.items():
            self.register_module(module, prefix)

    def register_func(self, func):
        if '_' in func.__name__:
            method, route = func.__name__.split('_', 1)
        else:
            method, route = func.__name__, ''

        method = method.upper()
        route = '/' + route.replace('__', '/')

        if method in {'GET', 'POST', 'PUT', 'DELETE'}:
            self.logger.info('Route: {} {}'.format(method, route))
            self.add_url_rule(route, func.__name__, func, methods=[method])

    def register_funcs(self, funcs):
        for func in funcs:
            self.register_func(func)
