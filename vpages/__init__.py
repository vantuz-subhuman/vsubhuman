from flask import session

import template_utils
from vutil import *


class VPages:
    __slots__ = ['routes', 'loginfn']

    def __init__(self, loginfn):
        self.routes = {}
        self.loginfn = loginfn

    def route(self, route, methods={'GET'}, login_required=False):
        def decorator(f):
            if route in self.routes:
                return raiseb('Route "%s" already exists!' % route)
            if login_required:
                def login_wrapper(*args, **kwargs):
                    if not session.get('logged_in'):
                        return self.loginfn(template_utils.url(route))
                    return f(*args, *kwargs)
                self.routes[route] = login_wrapper
                login_wrapper.rest_methods = conj_all({'POST'}, methods)
                return login_wrapper
            else:
                self.routes[route] = f
                f.rest_methods = methods
                return f
        return decorator

    def get_handler(self, route):
        return self.routes.get(route)

    @staticmethod
    def get_methods(f):
        return (f.rest_methods if hasattr(f, 'rest_methods') else None) or ['GET']