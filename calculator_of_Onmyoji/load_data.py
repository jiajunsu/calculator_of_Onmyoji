# coding: utf-8

import os
import traceback

import xlrd

import data_format


def get_excel_data(filename, sheet_name=u'御魂'):
    """Data format in Excel file: 
           data_format.EXCEL_COL_NAME_CN
    """
    if not os.path.exists(filename):
        print("文件不存在 ", filename)
        raise IOError("File not exists %s" % filename)

    try:
        xls_book = xlrd.open_workbook(filename=filename)
        data_sheet = xls_book.sheet_by_name(sheet_name)
        return data_sheet.get_rows() 
    except:
        print(traceback.format_exc())
        raise


def serialize_data(rows_data):
    mitama_data = dict()
    data_len = len(data_format.EXCEL_COL_NAME_CN)
    
    rows_data.next()  # skip first row
    for r_data in rows_data:
        serial = r_data[0].value
        data = dict()
        for i in range(1, data_len):
            prop_name = data_format.EXCEL_COL_NAME_EN[i]
            data[prop_name] = r_data[i].value

        mitama_data[serial] = data

    return mitama_data


if __name__ == '__main__':
    # for test
    d = get_excel_data('./example/data_Template.xlsx')
    m = serialize_data(d)
    print(m)
    for k,v in m.items():
        print(k, v)

