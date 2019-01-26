#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import traceback

import flask
from webob import exc

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
            res = {"reason": "Request content-type must be json"}
            return flask.make_response((json.dumps(res),
                                        exc.HTTPBadRequest.code))

        params = flask.request.get_json()
        calculator = cal_mitama.Calculator(params)
        result_num = calculator.run()
        ret = exc.HTTPOk.code
        res = {"result_num": result_num}
    except Exception:
        ret = exc.HTTPInternalServerError.code
        res = {"reason": traceback.format_exc()}

    return flask.make_response((json.dumps(res), ret))


if __name__ == '__main__':
    # TODO(jjs): load host and port from config file
    app.run(host='0.0.0.0', port=2019, debug=True)
