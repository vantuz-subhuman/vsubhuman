import os

from flask import Flask, request, render_template

import template_utils

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


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
    debug = os.environ.get('debug', 'true') == 'true'
    print('Debug: %s' % debug)
    app.run(debug=debug)
