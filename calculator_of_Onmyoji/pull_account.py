#!/usr/bin/python2
# coding: utf-8
from __future__ import print_function
import requests
import json
import xlwt


import data_format
from write_data import write_mitama_row

UASTRING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15"




def download_data(acc_id):       
    server_id = int(acc_id.split('-')[1])
    post_data = {'serverid':server_id, 'ordersn': acc_id}
    post_header = {'User Agent': UASTRING}
    post_url = 'https://yys.cbg.163.com/cgi/api/get_equip_detail'

    try:
        req = requests.post(post_url, data=post_data, headers=post_header)
        return req.json()
    except Exception as e:
        print('Unable to download the data.')
        return None


def generate_mitama_list(acc_id, filename, header_row=data_format.MITAMA_COL_NAME_ZH):
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
            mitama_pos = str(mitama_info['pos'])
            mitama_name = mitama_info['name']
            mitama_attrs = {i[0]:i[1] for i in mitama_info['attrs']}
            mitama_sheet.write(mitama_num, 0, label=mitama_id)
            mitama_sheet.write(mitama_num, 1, label=mitama_name)
            mitama_sheet.write(mitama_num, 2, label=mitama_pos)
            for i,prop in enumerate(data_format.MITAMA_PROPS):
                mitama_sheet.write(mitama_num, 3+i, label=mitama_attrs.get(prop, '').replace('%', ''))

            mitama_num += 1

        workbook.save(filename)
        print("write finish, we got %s results" % mitama_num)
    except Exception as e:
        print(e.message)
        raise e


def main():
    test_acc_id = "201806201301616-6-OBL2ZTNWBDPJYX"
    output_file = "data/cangbao.xls"
    generate_mitama_list(test_acc_id, output_file)


if __name__ == '__main__':
    main()
