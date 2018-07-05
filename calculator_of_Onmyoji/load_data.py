# coding: utf-8

import os
import traceback

import xlrd

from calculator_of_Onmyoji import data_format


def _get_sheet_rows(filename, sheet_name):
    if not os.path.exists(filename):
        print(u"文件不存在 ", filename)
        raise IOError("File not exists %s" % filename)

    try:
        xls_book = xlrd.open_workbook(filename=filename)
        data_sheet = xls_book.sheet_by_name(sheet_name)
        return data_sheet.get_rows()
    except Exception:
        print(traceback.format_exc())
        raise


def get_mitama_data(filename, ignore_serial):
    rows_data = _get_sheet_rows(filename, sheet_name=u'御魂')
    mitama_data = dict()
    data_len = len(data_format.MITAMA_COL_NAME_ZH)

    rows_data.next()  # skip first row
    for r_data in rows_data:
        serial = r_data[0].value

        if skip_serial(serial, ignore_serial):
            continue

        data = {data_format.MITAMA_COL_NAME_ZH[1]: r_data[1].value}

        for i in range(2, data_len):
            prop_name = data_format.MITAMA_COL_NAME_ZH[i]
            data[prop_name] = int(r_data[i].value) if r_data[i].value else 0

        mitama_data[serial] = data

    return mitama_data


def skip_serial(serial, ignore_list):
    for ig in ignore_list:
        if ig and isinstance(serial, (str, unicode)) and ig in serial:
            return True
    return False


def sep_mitama_by_loc(mitama_data):
    mitama_loc_data = {1: [], 2: [], 3: [],
                       4: [], 5: [], 6: []}

    for d_k, d_v in mitama_data.items():
        loc = d_v[u'位置']
        mitama_loc_data[loc].append({d_k: d_v})

    return mitama_loc_data


if __name__ == '__main__':
    # for test
    test_file = './example/data_Template.xls'
    d = get_mitama_data(test_file, [])
    print(d)
    l_d = sep_mitama_by_loc(d)
    print(l_d)
