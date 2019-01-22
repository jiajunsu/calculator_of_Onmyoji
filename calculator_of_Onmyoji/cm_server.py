#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

import flask

from calculator_of_Onmyoji import cal_mitama


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        calculator = cal_mitama.Calculator(flask.request.form.to_dict())
        calculator.run()
        return 'Calculate finished'
    except Exception:
        return traceback.format_exc()


if __name__ == '__main__':
    # TODO(jjs): load host and port from config file
    app.run(host='0.0.0.0', port=2019, debug=True)
