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
from flask_cors import CORS
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

CORS(app)
work_path = os.path.dirname(os.path.realpath(__file__))
calculator = None


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

        global calculator
        calculator = cal_mitama.Calculator(params)
        result_num = calculator.run()
        ret = exc.HTTPOk.code
        res = {"result_num": result_num,
               "output_file": params['output_file']}
    except IOError:
        ret = exc.HTTPForbidden.code
        res = {"reason": "Please check: 1.source_file exists;"
               " 2.output_file is writable and not be opened by other process."
               " %s" % traceback.format_exc()}
    except Exception:
        ret = exc.HTTPInternalServerError.code
        res = {"reason": traceback.format_exc()}

    return flask.make_response((json.dumps(res), ret))


@app.route('/status', methods=['GET'])
def status():
    if calculator:
        progress, current, total = calculator.get_progress()
    else:
        progress, current, total = 0, 0, 0

    res = {"status": "running"}
    if progress:
        res.update({"progress": progress,
                    "current": current,
                    "total": total})

    return flask.make_response((json.dumps(res)), 200)


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

    app.run(host=host, port=port, threaded=True)
