# coding: utf-8
import threading
import sys
import argparse
from calculator_of_Onmyoji import cm_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path",
                        type=str,
                        help='御魂数据所在文件夹')

    parser.add_argument("-P", "--port",
                        type=str,
                        default='2019',
                        help='服务器端口')

    parser.add_argument("-H", "--host",
                        type=str,
                        default='localhost',
                        help='服务器地址')

    args = parser.parse_args()

    cm_server.work_path = args.data_path

    t = threading.Thread(target=cm_server.open_browser,
                         args=(args.host, args.port))
    t.start()

    cm_server.app.run(host=args.host, port=args.port, threaded=True)

if __name__ == '__main__':
    main()
