#!/usr/bin/env python
# -*- coding:utf-8 -*-

import locale
from math import factorial
import itertools
import os

import xlrd
from xlutils.copy import copy

from calculator_of_Onmyoji.cal_and_filter import print_cal_rate
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

code_t = locale.getpreferredencoding()


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
            k = comb_dict_keys[i]
            if k == u'组合序号':
                try:
                    combs_data[k] = int(r_data[i].value)
                except ValueError:
                    combs_data[k] = r_data[i].value
            else:
                combs_data[k] = r_data[i].value

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
    n = len(mitama_combs)
    total = cal_comb_num(n, sub_comb_length)
    count = 0
    printed_rate = 0
    print('Calculating C(%s, %s) = %s' % (n, sub_comb_length, total))

    found_res = False
    for combs in itertools.combinations(mitama_combs, sub_comb_length):
        if is_non_repetitive_comb(combs):
            found_res = True
            write_single_comb_data(combs)
        count += 1
        printed_rate = print_cal_rate(count, total, printed_rate, rate=10)

    return found_res


def cal_comb_num(n, m):
    '''计算组合数

    C(n, m) = n!/((n-m)! * m!)
    '''
    x = 1
    for i in xrange(n, m, -1):
        x *= i
    x /= factorial(n - m)

    return x


def find_all_independent_combs(mitama_combs, expect_counts):
    if expect_counts == 0:
        for c in xrange(2, len(mitama_combs)):
            # 从2开始遍历，直至无法再找到独立组合
            if not make_independent_comb(mitama_combs, c):
                break
    else:
        make_independent_comb(mitama_combs, expect_counts)


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


def input_expect_combs_counts():
    prompt = get_encode_str(u'请输入期望的独立套装个数并回车'
                            u'(0为计算所有可能): ')
    input = raw_input(prompt)
    try:
        expect_counts = int(input)
        if expect_counts < 2 and expect_counts != 0:
            raise ValueError
    except Exception:
        exc_prompt = get_encode_str(u'输入必须为0或大于等于2的整数')
        print(exc_prompt)
        exit(1)

    return expect_counts


def get_encode_str(ustr):
    return ustr.encode(code_t)


def main():
    xls_files = load_data.get_ext_files('.xls')
    result_files = [f for f in xls_files
                    if '-result' in f and 'comb' not in f]

    print('Files below will be calculated:\n%s\n' % result_files)
    expect_counts = input_expect_combs_counts()

    for file_name in result_files:
        print('Calculating %s' % file_name)
        mitama_combs = load_result(file_name)

        init_write_book(file_name)
        find_all_independent_combs(mitama_combs, expect_counts)
        save_write_book(file_name)

        if work_sheet_num >= 1:
            independent_combs_num = (write_data.MAX_ROW * (work_sheet_num - 1)
                                     + row_num - 1)
        elif row_num >= 1:
            independent_combs_num = row_num - 1
        else:
            independent_combs_num = row_num

        print('Calculating finish, get %s independent combinations'
              % independent_combs_num)


if __name__ == '__main__':
    main()

    raw_input('Press any key to exit')
