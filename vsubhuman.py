import os

from flask import Flask, request, render_template, redirect, url_for, session

import template_utils
from vutil import *

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'dev')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login') + '?redirect=%s' % url_for('admin'))
    return render_template('admin.html', user=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        logout, login, password, target = destruct(request.form, 'logout', 'login', 'password', 'redirect')
        if logout:
            session['logged_in'] = False
            session['user'] = None
        if not empty(login):
            if login == 'admin' and password == 'admin':
                session['logged_in'] = True
                session['user'] = {'login': login}
                return redirect(target or url_for('index'))
            else:
                error = 'Incorrect login or password'
    return render_template('login.html', error=error)


@app.route('/tag/<path:id>')
def tag(id):
    return '<html><body><h1>Path: "%s"</h1></body></html>' % id.lower().split('/')


@app.route('/uc')
def uc():
    back = None
    if request.args.get('noback') != '1':
        back_url = request.args.get('back_url') or '/'
        back_name = request.args.get('back_name') or 'homepage'
        back = {'url': back_url, 'name': back_name}
    return render_template('uc.html', back=back)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


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
