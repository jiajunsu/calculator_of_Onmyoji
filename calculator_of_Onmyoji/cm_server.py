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
        # NOTE: request must be "Content-Type: application/json"
        if not flask.request.is_json:
            return flask.make_response(('Request content-type must be json',
                                        400))
        params = flask.request.get_json()
        calculator = cal_mitama.Calculator(params)
        calculator.run()
        return flask.make_response(('Calculate finished', 200))
    except Exception:
        return flask.make_response((traceback.format_exc(), 500))


if __name__ == '__main__':
    # TODO(jjs): load host and port from config file
    app.run(host='0.0.0.0', port=2019, debug=True)
