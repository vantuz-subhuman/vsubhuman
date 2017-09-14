import os

from flask import Flask, request, render_template, redirect, session

import template_utils
from vutil import *

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'dev')


class VPages:
    __slots__ = ['routes']

    def __init__(self):
        self.routes = {}

    def route(self, route, methods={'GET'}, login_required=False):
        def decorator(f):
            if route in self.routes:
                return raiseb('Route "%s" already exists!' % route)
            if login_required:
                def login_wrapper(*args, **kwargs):
                    if not session.get('logged_in'):
                        return login(template_utils.url(route))
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


vpages = VPages()


@vpages.route('/login', methods={'GET', 'POST'})
def login(target=None):
    error = None
    if request.method == 'POST':
        logout, login, password = destruct(request.form, 'logout', 'login', 'password')
        if logout:
            session['logged_in'] = False
            session['user'] = None
        if not empty(login):
            if login == 'admin' and password == 'admin':
                session['logged_in'] = True
                session['user'] = {'login': login}
                return redirect(target or template_utils.url(''))
            else:
                error = 'Incorrect login or password'
    return render_template('login.html', redirect=(target is not None), error=error)


@vpages.route('/admin', login_required=True)
def admin():
    return render_template('admin.html', user=session['user'])


@vpages.route('/uc')
def uc():
    back = None
    if request.args.get('noback') != '1':
        back_url = request.args.get('back_url') or '/'
        back_name = request.args.get('back_name') or 'homepage'
        back = {'url': back_url, 'name': back_name}
    return render_template('uc.html', back=back)


@vpages.route('/')
def index():
    return render_template('index.html')


@vpages.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html')


@app.route('/')
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path=None):
    f = vpages.get_handler('/%s' % (path or ''))
    if request.method not in VPages.get_methods(f):
        return method_not_allowed(None)
    return f() if f else page_not_found(None)


@app.context_processor
def context():
    return dict(
        static=template_utils.static,
        static_root=template_utils.static_root,
        url=template_utils.url
    )


if __name__ == '__main__':
    print('Starting app in debug mode')
    app.run(debug=True)
