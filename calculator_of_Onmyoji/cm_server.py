#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
import json
import os
import sys
import threading
import time
import traceback
import webbrowser

import flask
from webob import exc

from calculator_of_Onmyoji import cal_mitama


if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys.executable, '..', 'templates')
    static_folder = os.path.join(sys.executable, '..', 'static')
    app = flask.Flask(__name__,
                      template_folder=template_folder,
                      static_folder=static_folder)
else:
    app = flask.Flask(__name__)

work_path = os.path.dirname(os.path.realpath(__file__))


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
            dst_filename = os.path.splitext(src_filename)[0] + '-result.xls'
            params['source_data'] = os.path.join(work_path, src_filename)
            params['output_file'] = os.path.join(work_path, dst_filename)

        calculator = cal_mitama.Calculator(params)
        result_num = calculator.run()
        ret = exc.HTTPOk.code
        res = {"result_num": result_num,
               "output_file": params['output_file']}
    except Exception:
        ret = exc.HTTPInternalServerError.code
        res = {"reason": traceback.format_exc()}

    return flask.make_response((json.dumps(res), ret))


def open_browser(host, port):
    url = 'http://%s:%s' % (host, port)
    time.sleep(1)
    webbrowser.open(url)


if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(work_path, 'server.conf'))
    host = conf.get('global', 'host')
    port = conf.get('global', 'port')

    t = threading.Thread(target=open_browser, args=(host, port))
    t.start()

    app.run(host=host, port=port)
