#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
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

        if 'src_filename' in params:
            # NOTE: UI只能获取文件名，限定文件必须在当前目录
            src_filename = params['src_filename']
            dst_filename = '-result'.join(os.path.splitext(src_filename))
            work_path = os.getcwd()
            params['source_data'] = os.path.join(work_path, src_filename)
            params['output_file'] = os.path.join(work_path, dst_filename)

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
