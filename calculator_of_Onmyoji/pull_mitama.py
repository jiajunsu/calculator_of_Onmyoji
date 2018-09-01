#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import json
import traceback

import requests
import xlwt

from calculator_of_Onmyoji import data_format

UASTRING = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 "
            "Safari/605.1.15")

parser = argparse.ArgumentParser()
parser.add_argument("acc_id",
                    type=str,
                    help=u'藏宝阁id，商品详情页面对应的网址中，'
                         u'格式如201806211901616-3-KJ8J8IQOJTOMD8')
parser.add_argument("-O", "--output-file",
                    type=str,
                    default='mitama_data.xls',
                    help=u'输出文件位置，格式为pathto/filename.xls')


def download_data(acc_id):
    server_id = int(acc_id.split('-')[1])
    post_data = {'serverid': server_id, 'ordersn': acc_id}
    post_header = {'User Agent': UASTRING}
    post_url = 'https://yys.cbg.163.com/cgi/api/get_equip_detail'

    try:
        print(post_url, post_data, post_header)
        req = requests.post(post_url, data=post_data, headers=post_header,
                            verify=False)
        return json.loads(req.text)
    except Exception:
        print('Unable to download the data. %s' % traceback.format_exc())
        return None


def generate_mitama_list(acc_id, filename,
                         header_row=data_format.MITAMA_COL_NAME_ZH):
    print("Downloading data...")
    res = download_data(acc_id)

    print("Dumping mitama data...")
    if res is None:
        return

    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        mitama_sheet = workbook.add_sheet(u'御魂')
        acct_info = res['equip']
        acct_detail = json.loads(acct_info['equip_desc'])

        mitama_list = acct_detail['inventory']

        col_nums = len(header_row)

        # write header row
        for c in range(col_nums):
            mitama_sheet.write(0, c, label=header_row[c])

        mitama_num = 1
        for mitama_id in mitama_list:
            mitama_info = mitama_list[mitama_id]
            if int(mitama_info['level']) < 15:
                continue
            mitama_pos = str(mitama_info['pos'])
            mitama_name = mitama_info['name']
            mitama_attrs = dict()
            # 获取首领御魂独立属性
            single_prop = mitama_info.get('single_attr')
            if single_prop:
                mitama_attrs[single_prop[0]] = int(
                    single_prop[1].replace('%', ''))
            for prop, value in mitama_info['attrs']:
                value = int(value.replace('%', ''))
                if prop not in mitama_attrs:
                    mitama_attrs[prop] = value
                else:
                    mitama_attrs[prop] += value

            mitama_sheet.write(mitama_num, 0, label=mitama_id)
            mitama_sheet.write(mitama_num, 1, label=mitama_name)
            mitama_sheet.write(mitama_num, 2, label=mitama_pos)
            for i, prop in enumerate(data_format.MITAMA_PROPS):
                prop_value = mitama_attrs.get(prop, '')
                mitama_sheet.write(mitama_num, 3+i, label=prop_value)

            mitama_num += 1

        workbook.save(filename)
        print("write finish, we got %s results" % mitama_num)
    except Exception as e:
        print(e.message)
        raise e


def main():
    args = parser.parse_args()
    test_acc_id = args.acc_id
    output_file = args.output_file
    print('Start pulling mitama data, please wait')
    generate_mitama_list(test_acc_id, output_file)


if __name__ == '__main__':
    main()
