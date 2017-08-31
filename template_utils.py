from flask.helpers import url_for

from vutil import *


def static_root(path):
    return P(static, path=path)


def static(file, path=None):
    pref = path + '/' if not empty(path) else ''
    return url('static', filename=(pref + file))


def url(endpoint, **values):
    return url_for(endpoint, _external=True, **values)