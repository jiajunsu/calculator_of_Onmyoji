# coding: utf-8

import os
import traceback

import xlrd

from calculator_of_Onmyoji import data_format


def _get_sheet_rows(filename, sheet_name):
    if not os.path.exists(filename):
        print("文件不存在 ", filename)
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

        data = dict()
        for i in range(1, data_len):
            prop_name = data_format.MITAMA_COL_NAME_ZH[i]
            data[prop_name] = r_data[i].value

        mitama_data[serial] = data

    return mitama_data


def skip_serial(serial, ignore_list):
    for ig in ignore_list:
        if ig and isinstance(serial, (str, unicode)) and ig in serial:
            return True
    return False


def get_mitama_enhance(filename):
    rows_data = _get_sheet_rows(filename, sheet_name=u'御魂类别')
    mitama_en_prop = dict()

    rows_data.next()  # skip first row
    for r_data in rows_data:
        mitama_name = r_data[0].value
        data = {u'加成类型': r_data[1].value,
                u'加成数值': r_data[2].value}
        mitama_en_prop[mitama_name] = data

    return mitama_en_prop


def sep_mitama_by_loc(mitama_data):
    mitama_loc_data = {1: [], 2: [], 3: [],
                       4: [], 5: [], 6: []}

    for d_k, d_v in mitama_data.items():
        loc = int(d_v[u'位置'])
        mitama_loc_data[loc].append({d_k: d_v})

    return mitama_loc_data


if __name__ == '__main__':
    # for test
    test_file = './example/data_Template.xlsx'
    d = get_mitama_data(test_file)
    print(d)
    l_d = sep_mitama_by_loc(d)
    print(l_d)

    p = get_mitama_enhance(test_file)
    for k, v in p.items():
        print(k, v)
