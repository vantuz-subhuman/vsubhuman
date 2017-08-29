from flask import Flask, request, render_template

import template_utils
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('uc.html')


@app.route('/uc')
def uc():
    back = None
    if request.args.get('noback') != '1':
        back_url = request.args.get('back_url') or '/'
        back_name = request.args.get('back_name') or 'homepage'
        back = {'url': back_url, 'name': back_name}
    return render_template('uc.html', back=back)


@app.context_processor
def context():
    return dict(
        static=template_utils.static,
        static_root=template_utils.static_root
    )


if __name__ == '__main__':
    debug = os.environ.get('debug', 'true') == 'true'
    print('Debug: %s' % debug)
    app.run(debug=debug)
