#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

import xlrd
from xlutils.copy import copy

from calculator_of_Onmyoji import cal_and_filter
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


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
    work_sheet = write_book.add_sheet(u'indepenent_combs_%s' % work_sheet_num)
    write_data.write_header_row(work_sheet, 'result_combs')
    row_num = 1

    for combs in independent_combs:
        work_sheet.write(row_num, 0, combs[u'组合个数'])
        work_sheet.write(row_num, 1, combs[u'result序号'])
        work_sheet.write(row_num, 2, combs[u'攻击x暴伤'])
        work_sheet.write(row_num, 3, combs[u'速度'])
        row_num += 1

        if row_num > 65535:
            work_sheet_num += 1
            work_sheet = write_book.add_sheet(u'indepenent_combs_%s'
                                              % work_sheet_num)
            write_data.write_header_row(work_sheet, 'result_combs')

    file_name, file_extension = os.path.splitext(filename)
    result_file = file_name + '-comb' + file_extension

    write_book.save(result_file)


def search_independent_comb(mitama_combs):
    used_mitama = []
    independent_comb = []
    for combs_data in mitama_combs:
        mitama_serials = combs_data.get(u'御魂序号', '').split(',')
        if not (set(used_mitama) & set(mitama_serials)):
            # 无重复御魂，即为独立组合
            # Note: 第一个组合永远会加入
            independent_comb.append(combs_data)
            used_mitama.extend(mitama_serials)

    return independent_comb


def make_independent_comb(mitama_combs):
    calculated_count = 0
    printed_rate = 0
    total_comb = len(mitama_combs)
    sys.stdout.flush()

    independent_comb_list = []
    while mitama_combs:
        # 以第一个组合为基础，计算所有的独立套装
        independent_comb = search_independent_comb(mitama_combs)
        if len(independent_comb) > 1:
            result_comb_data = gen_result_comb_data(independent_comb)
            independent_comb_list.append(result_comb_data)
        mitama_combs.pop(0)

        calculated_count += 1
        printed_rate = cal_and_filter.print_cal_rate(calculated_count,
                                                     total_comb, printed_rate)

    return independent_comb_list


def gen_result_comb_data(independent_comb):
    result_serials = []
    attack_values = []
    speed_values = []

    for comb_data in independent_comb:
        result_serials.append(str(comb_data.get(u'组合序号', 0)))
        attack_values.append(str(comb_data.get(u'攻击x暴伤', 0)))
        speed_values.append(str(comb_data.get(u'速度', 0)))

    result_comb_data = {u'组合个数': len(independent_comb),
                        u'result序号': ','.join(result_serials),
                        u'攻击x暴伤': ','.join(attack_values),
                        u'速度': ','.join(speed_values),
                        }
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
