#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itertools
import os

import xlrd
from xlutils.copy import copy

from calculator_of_Onmyoji import data_format
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


work_sheet = None
row_num = 0

global work_sheet
global row_num


def load_result(filename):
    xls_book = xlrd.open_workbook(filename=filename, on_demand=True)
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


def write_independent_comb_result(filename, independent_combs):
    read_book = xlrd.open_workbook(filename=filename)
    write_book = copy(read_book)

    work_sheet_num = 0
    global work_sheet
    work_sheet = write_book.add_sheet(u'indepenent_combs_%s' % work_sheet_num)
    write_data.write_header_row(work_sheet, 'result_combs')
    row_num = 1

    for combs in independent_combs:
        work_sheet.write(row_num, 0, combs[u'组合个数'])
        work_sheet.write(row_num, 1, combs[u'result序号'])
        work_sheet.write(row_num, 2, combs[u'暴击'])
        work_sheet.write(row_num, 3, combs[u'攻击x暴伤'])
        work_sheet.write(row_num, 4, combs[u'速度'])
        row_num += 1

        if row_num > 65535:
            work_sheet_num += 1
            work_sheet = write_book.add_sheet(u'indepenent_combs_%s'
                                              % work_sheet_num)
            write_data.write_header_row(work_sheet, 'result_combs')

    file_name, file_extension = os.path.splitext(filename)
    result_file = file_name + '-comb' + file_extension

    write_book.save(result_file)


def get_mitama_serials(combs_data):
    return combs_data.get(u'御魂序号', '').split(',')


def is_non_repetitive_comb(mitama_combs):
    seed_serials = set()

    for combs_data in mitama_combs:
        mitama_serials = set(get_mitama_serials(combs_data))
        if seed_serials & mitama_serials:
            return False
        else:
            seed_serials |= mitama_serials

    return True


def make_independent_comb(mitama_combs, sub_comb_length):
    '''遍历组合，找出独立组合并触发写数据'''
    for combs in itertools.combinations(mitama_combs, sub_comb_length):
        if is_non_repetitive_comb(combs):
            write_single_comb_data(combs)


def write_single_comb_data(combs):
    global row_num
    row_num += 1

    result_comb_data = gen_result_comb_data(combs)

    col_num = 0
    for col_name in data_format.RESULT_COMB_HEADER:
        work_sheet.write(row_num, col_num, result_comb_data.get(col_name, ''))
        col_num += 1


def gen_result_comb_data(independent_comb):
    result_comb_data = {u'组合个数': len(independent_comb)}

    for key in data_format.RESULT_COMB_HEADER[1:]:
        result_comb_data[key] = ','.join([str(d.get(key, 0))
                                          for d in independent_comb])

    return result_comb_data


if __name__ == '__main__':
    xls_files = load_data.get_ext_files('.xls')
    result_files = [f for f in xls_files if '-result' in f]

    for file_name in result_files:
        print('Calculating %s' % file_name)
        mitama_combs = load_result(file_name)
        independent_combs = make_independent_comb(mitama_combs)
        write_independent_comb_result(file_name, independent_combs)
        print('Calculating finish, get %s independent combinations'
              % len(independent_combs))

    raw_input('Press any key to exit')
