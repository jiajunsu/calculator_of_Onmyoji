#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itertools
import os

import xlrd
from xlutils.copy import copy

from calculator_of_Onmyoji import data_format
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


global write_book
global work_sheet
global work_sheet_num
global row_num

write_book = None
work_sheet = None
work_sheet_num = 0
row_num = 0


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


def init_write_book(filename):
    global write_book
    read_book = xlrd.open_workbook(filename=filename)
    write_book = copy(read_book)


def init_work_sheet():
    global work_sheet
    global work_sheet_num
    global row_num
    work_sheet = write_book.add_sheet(u'indepenent_combs_%s' % work_sheet_num)
    work_sheet_num += 1

    write_data.write_header_row(work_sheet, 'result_combs')
    row_num = 1


def save_write_book(filename):
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
    if not work_sheet or row_num > write_data.MAX_ROW:
        init_work_sheet()

    result_comb_data = gen_result_comb_data(combs)

    col_num = 0
    for col_name in data_format.RESULT_COMB_HEADER:
        work_sheet.write(row_num, col_num, result_comb_data.get(col_name, ''))
        col_num += 1

    row_num += 1


def gen_result_comb_data(independent_comb):
    result_comb_data = {u'组合个数': len(independent_comb)}

    for key in data_format.RESULT_COMB_HEADER[1:]:
        result_comb_data[key] = ','.join([str(d.get(key, 0))
                                          for d in independent_comb])

    return result_comb_data


def input_expect_combs_length():
    input = raw_input('请输入期望的独立套装个数并回车: ')
    try:
        sub_comb_length = int(input)
        if sub_comb_length < 0:
            raise ValueError
    except Exception:
        print('输入必须为非负整数')
        exit(1)

    return sub_comb_length


if __name__ == '__main__':
    sub_comb_length = input_expect_combs_length()

    xls_files = load_data.get_ext_files('.xls')
    result_files = [f for f in xls_files if '-result' in f]

    for file_name in result_files:
        print('Calculating %s' % file_name)
        mitama_combs = load_result(file_name)

        init_write_book(file_name)
        make_independent_comb(mitama_combs, sub_comb_length)
        save_write_book(file_name)

        independent_combs_num = (write_data.MAX_ROW * (work_sheet_num - 1)
                                 + row_num - 1)

        print('Calculating finish, get %s independent combinations'
              % len(independent_combs_num))

    raw_input('Press any key to exit')
