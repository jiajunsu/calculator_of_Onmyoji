#!/usr/bin/env python
# -*- coding:utf-8 -*-

import flask

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if flask.request.method == 'POST':
        # TODO(jjs): start calculator
        return ''
    else:
        # TODO(jjs): get the process of calculator
        return ''


if __name__ == '__main__':
    # TODO(jjs): load host and port from config file
    app.run(host='0.0.0.0', port=2019)
