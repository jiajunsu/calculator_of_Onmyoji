#!/usr/bin/env python
# -*- coding:utf-8 -*-

from itertools import combinations
import locale
from math import factorial
import multiprocessing
import os
import traceback

from tqdm import tqdm
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
            elif k == u'御魂序号':
                # 直接转换为set，减少循环内的计算
                combs_data[k] = set(r_data[i].value.split(','))
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


def get_non_repetitive_comb(mitama_combs):
    seed_serials = set()

    for combs_data in mitama_combs:
        mitama_serials = combs_data.get(u'御魂序号')
        if seed_serials & mitama_serials:
            return None
        else:
            seed_serials |= mitama_serials

    return mitama_combs


def make_independent_comb(mitama_combs, sub_comb_length, cores):
    '''遍历组合，找出独立组合并触发写数据'''
    n = len(mitama_combs)
    total = cal_comb_num(n, sub_comb_length)
    print('Calculating C(%s, %s) = %s' % (n, sub_comb_length, total))

    found_res = False

    if cores > 1:
        p = multiprocessing.Pool(processes=cores)
        found_res = False
        # TODO: 将更多步骤放到imap里面去做，不仅仅是判断是否独立
        for combs in tqdm(p.imap_unordered(get_non_repetitive_comb,
                                           combinations(mitama_combs,
                                                        sub_comb_length)),
                          desc='Calculating', total=total, unit='comb'):
            if combs:
                found_res = True
                write_single_comb_data(combs)
        p.close()
        p.join()
        del p
    else:
        for combs in tqdm(combinations(mitama_combs, sub_comb_length),
                          desc='Calculating', total=total, unit='comb'):
            if get_non_repetitive_comb(combs):
                found_res = True
                write_single_comb_data(combs)

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


def find_all_independent_combs(mitama_combs, expect_counts,
                               use_multi_process):
    if use_multi_process:
        cores = multiprocessing.cpu_count()
    else:
        cores = 1

    print('Use CPU cores number %s' % cores)
    if expect_counts == 0:
        for c in xrange(2, len(mitama_combs)):
            # 从2开始遍历，直至无法再找到独立组合
            if not make_independent_comb(mitama_combs, c, cores):
                break
    else:
        make_independent_comb(mitama_combs, expect_counts, cores)


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
        os.exit(1)

    return expect_counts


def input_use_multi_process():
    prompt = get_encode_str(u'是否使用多进程计算(电脑会比较卡) y/n: ')
    input = raw_input(prompt)
    if input.strip().lower() == 'y':
        return True
    else:
        return False


def get_encode_str(ustr):
    return ustr.encode(code_t)


def main():
    xls_files = load_data.get_ext_files('.xls')
    result_files = [f for f in xls_files
                    if '-result' in f and 'comb' not in f]

    if not result_files:
        print('No files with postfix "-result.xls" found.')
        return

    print('Files below will be calculated:\n%s\n' % result_files)
    expect_counts = input_expect_combs_counts()
    # TODO: 将更多步骤放到imap里面去做，然后再打开多进程开关
#    use_multi_process = input_use_multi_process()
    use_multi_process = False

    for file_name in result_files:
        print('Calculating %s' % file_name)
        mitama_combs = load_result(file_name)

        init_write_book(file_name)
        find_all_independent_combs(mitama_combs, expect_counts,
                                   use_multi_process)
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
    multiprocessing.freeze_support()  # For windows platform

    try:
        main()
    except Exception:
        print(traceback.format_exc())
    finally:
        raw_input('\nPress any key to exit')
