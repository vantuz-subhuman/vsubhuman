import os

from flask import Flask, request, render_template, redirect, url_for, session

import template_utils
from vutil import *

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'dev')


class Methods:
    def __init__(self, *methods):
        self.methods = methods

    def __call__(self, f):
        f.rest_methods = self.methods
        return f


def home():
    return render_template('index.html')


def about():
    return render_template('about.html')


@Methods('GET', 'POST')
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


@Methods('GET', 'POST')
def admin():
    if not session.get('logged_in'):
        return login(template_utils.url('admin'))
    return render_template('admin.html', user=session['user'])


def uc():
    back = None
    if request.args.get('noback') != '1':
        back_url = request.args.get('back_url') or '/'
        back_name = request.args.get('back_name') or 'homepage'
        back = {'url': back_url, 'name': back_name}
    return render_template('uc.html', back=back)


routes = {
    '': home,
    'about': about,
    'admin': admin,
    'login': login,
    'uc': uc
}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html')


@app.route('/')
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path=None):
    f = routes.get(path or '')
    if request.method not in getattr(f, 'rest_methods', ['GET']):
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
