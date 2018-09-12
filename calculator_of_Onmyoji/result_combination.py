#!/usr/bin/env python
# -*- coding:utf-8 -*-

from xlutils.copy import copy
import xlrd
import xlwt


def load_result(filename):
    xls_book = xlrd.open_workbook(filename=filename)
    data_sheet = xls_book.sheet_by_name('result')
    rows_data = data_sheet.get_rows()

    comb_dict_keys = []
    r_data = rows_data.next()  # first row is key name
    for k in r_data:
        comb_dict_keys.append(k.value)

    mitama_combs = []

    for r_data in rows_data:
        combs_data = dict()
        for i in range(len(comb_dict_keys)):
            combs_data[comb_dict_keys[i]] = r_data[i].value

        mitama_combs.append(combs_data)

    return mitama_combs


def write_independent_comb_result(filename, independet_combs):
    pass


def sort_mitama_combs(mitama_combs, sort_key=u'攻击x暴伤'):
    pass


def search_independent_combs(mitama_combs):
    pass


if __name__ == '__main__':
    import sys

    load_result(sys.argv[1])
