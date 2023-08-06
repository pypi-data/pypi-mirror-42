import re
import inspect
import importlib


def func_parse(module):
    """
    Why we use module_parse instead of module.__dict__?
    module.__dict__ contains more variables from imported files, that's what we won't it happen.
    """
    regex = re.compile(r'^def (\w+)\(')
    funcs = []
    for line in inspect.getsource(module).split('\n'):
        match = re.match(regex, line)
        if match:
            funcs.append(match.group(1))
    return funcs


def module_parse(import_name):
    route_args = []
    before_request = None

    if not import_name:
        return route_args, before_request

    if isinstance(import_name, str):
        module = importlib.import_module(import_name)
    else:
        module = import_name

    for name in func_parse(module):
        if name.startswith('_'):
            continue

        if name == 'before_request':
            before_request = getattr(module, name)

        if '_' in name:
            method, route = name.split('_', 1)
        else:
            method, route = name, ''

        method = method.upper()
        route = '/' + route.replace('__', '/')

        if method in {'GET', 'POST', 'PUT', 'DELETE'}:
            route_args.append(dict(rule=route, endpoint=name, view_func=getattr(module, name), methods=[method]))

    return route_args, before_request
