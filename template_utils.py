from flask.helpers import url_for

from vutil import *


def static_root(path):
    return P(static, path=path)


def static(file, path=None):
    pref = path + '/' if not empty(path) else ''
    return url_for('static', filename=(pref + file), _external=True)