#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import csv
from itertools import combinations
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


class ResultBook(object):
    def __init__(self, filename, postfix):
        self.filename = filename
        self.postfix = str(postfix)

        read_book = xlrd.open_workbook(filename=self.filename)
        self.write_book = copy(read_book)

        self.work_sheet = None
        self.work_sheet_num = 0
        self.row_num = 0
        self.count = 0

    def init_work_sheet(self):
        self.work_sheet = self.write_book.add_sheet('independent_combs_%s'
                                                    % self.work_sheet_num)
        self.work_sheet_num += 1

        write_data.write_header_row(self.work_sheet, 'result_combs')
        self.row_num = 1

    def write(self, comb_data):
        if not self.work_sheet or self.row_num > write_data.MAX_ROW:
            self.init_work_sheet()

        col_num = 0
        for col_name in data_format.RESULT_COMB_HEADER:
            self.work_sheet.write(self.row_num, col_num,
                                  comb_data.get(col_name, ''))
            col_num += 1

        self.row_num += 1
        self.count += 1

    def save(self):
        file_name, file_extension = os.path.splitext(self.filename)
        result_file = ''.join([file_name, '-comb', '_', self.postfix,
                               file_extension])

        self.write_book.save(result_file)


class ResultBookCSV(object):
    """Write comb result into .csv file.

    Attributes:
        count (int): comb nums of result book.
        filename (str): File name
        postfix (str or int): postfix to seperate this file from
            original mitama combs.
        write_book (_io.TextIOWrapper): file descriptor.
        writer (csv.DictWriter): csv.DictWriter
    """

    def __init__(self, filename, postfix):
        self.postfix = str(postfix)
        self.filename = filename[:-4] + '-comb_' + self.postfix + '.csv'
        # Avoid messy code in win platform
        with open(self.filename, 'wb') as fd:
            fd.write(codecs.BOM_UTF8)
        self.write_book = open(self.filename, 'a',
                               newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.write_book,
                                     data_format.RESULT_COMB_HEADER)
        self.writer.writeheader()
        self.count = 0

    def write(self, comb_data):
        self.writer.writerow(comb_data)
        self.count += 1

    def save_and_close(self):
        self.write_book.close()


class MakeResultInPool(object):
    def __init__(self, filename, postfix):
        self.filename = filename
        self.postfix = str(postfix)

        self.result_book = dict()

    def _get_result_book(self):
        pid = os.getpid()
        res_book = self.result_book.get(pid)
        if not res_book:
            res_book = ResultBook(self.filename,
                                  ''.join([str(pid), '_', self.postfix]))
            self.result_book[pid] = res_book
        return res_book

    def __call__(self, mitama_combs):
        comb_data = get_independent_comb_data(mitama_combs)
        if comb_data:
            res_book = self._get_result_book()
            res_book.write(comb_data)

    def save(self):
        for res_book in self.result_book.values():
            res_book.save()

    @property
    def count(self):
        count = 0
        for res_book in self.result_book.values():
            count += res_book.count
        return count


def load_result_sheet(filename):
    xls_book = xlrd.open_workbook(filename=filename, on_demand=True)
    data_sheet = xls_book.sheet_by_name('result')
    rows_data = data_sheet.get_rows()

    comb_dict_keys = []
    r_data = next(rows_data)  # first row is key name
    for k in r_data:
        comb_dict_keys.append(k.value)

    mitama_combs = []

    for r_data in rows_data:
        combs_data = dict()
        for i in range(len(comb_dict_keys)):
            k = comb_dict_keys[i]
            if k == '组合序号':
                try:
                    combs_data[k] = int(r_data[i].value)
                except ValueError:
                    combs_data[k] = r_data[i].value
            elif k == '御魂序号':
                # 直接转换为set，减少循环内的计算
                combs_data[k] = set(r_data[i].value.split(','))
            else:
                combs_data[k] = r_data[i].value

        mitama_combs.append(combs_data)

    return mitama_combs


def load_comb_result_sheet(filename):
    """load .csv comb file into memory. Not used in this version.

    Args:
        filename (str): File name to be loaded

    Returns:
        combs_data(list of OrderedDict): data of mitama combs.
    """
    print("Loading previous result: %s" % filename)
    with open(filename, 'r') as fd:
        reader = csv.DictReader(fd)
        # print(reader.fieldnames)
        combs_data = list(reader)
    return combs_data


def get_independent_comb_data(mitama_combs):
    seed_serials = set()

    for combs_data in mitama_combs:
        mitama_serials = combs_data.get('御魂序号')
        if seed_serials & mitama_serials:
            return None
        else:
            seed_serials |= mitama_serials

    return gen_result_comb_data(mitama_combs)


def make_independent_comb(file_name, mitama_combs, sub_comb_length, cores):
    '''遍历组合，找出独立组合并触发写数据'''
    n = len(mitama_combs)
    total = cal_comb_num(n, sub_comb_length)
    print('Calculating C(%s, %s) = %s' % (n, sub_comb_length, total))

    if cores > 1:
        p = multiprocessing.Pool(processes=cores)
        # TODO(jjs): 这种方式性能太差，改用Queue模式
        make_comb_data_parallel = MakeResultInPool(file_name, sub_comb_length)
        for _ in tqdm(p.imap_unordered(make_comb_data_parallel,
                                       combinations(mitama_combs,
                                                    sub_comb_length)),
                      desc='Calculating', total=total, unit='comb'):
            pass
        p.close()
        p.join()
        del p
        make_comb_data_parallel.save()
        return make_comb_data_parallel.count
    else:
        result_book = ResultBookCSV(file_name, sub_comb_length)
        for combs in tqdm(combinations(mitama_combs, sub_comb_length),
                          desc='Calculating', total=total, unit='comb'):
            comb_data = get_independent_comb_data(combs)
            if comb_data:
                result_book.write(comb_data)

        result_book.save_and_close()
        return result_book.count


def cal_comb_num(n, m):
    '''计算组合数

    C(n, m) = n!/((n-m)! * m!)
    '''
    x = 1
    for i in range(n, m, -1):
        x *= i
    x /= factorial(n - m)

    return x


def make_all_independent_combs(file_name, mitama_combs, expect_counts,
                               use_multi_process):
    if use_multi_process:
        cores = multiprocessing.cpu_count()
    else:
        cores = 1

    print('Use CPU cores number %s' % cores)
    if expect_counts == 0:
        combs_count = 0
        for c in range(2, len(mitama_combs)):
            # 从2开始遍历，直至无法再找到独立组合
            res_count = make_independent_comb(file_name,
                                              mitama_combs, c, cores)
            if res_count == 0:
                break
            combs_count += res_count
    else:
        combs_count = make_independent_comb(file_name,
                                            mitama_combs, expect_counts, cores)

    return combs_count


def gen_result_comb_data(independent_comb):
    result_comb_data = {'组合个数': len(independent_comb)}

    for key in data_format.RESULT_COMB_HEADER[1:]:
        result_comb_data[key] = ','.join([str(d.get(key, 0))
                                          for d in independent_comb])

    return result_comb_data


def input_expect_combs_counts():
    prompt = '请输入期望的独立套装个数并回车(0为计算所有可能): '
    inputchar = input(prompt)
    try:
        expect_counts = int(inputchar)
        if expect_counts < 2 and expect_counts != 0:
            raise ValueError
    except Exception:
        print('输入必须为0或大于等于2的整数')
        os.exit(1)
    return expect_counts


def input_use_multi_process():
    inputchar = input('是否使用多进程计算(电脑会比较卡) y/n: ')
    if inputchar.strip().lower() == 'y':
        return True
    else:
        return False


def main():
    xls_files = load_data.get_ext_files('.xls')
    result_files = [f for f in xls_files
                    if '-result' in f and 'comb' not in f]

    if not result_files:
        print('No files with postfix "-result.xls" found.')
        return

    print('Files below will be calculated:\n%s\n' % result_files)
    expect_counts = input_expect_combs_counts()
    # TODO(jjs): 将更多步骤放到imap里面去做，然后再打开多进程开关
#    use_multi_process = input_use_multi_process()
    use_multi_process = False

    for file_name in result_files:
        print('Calculating %s' % file_name)
        mitama_combs = load_result_sheet(file_name)
        combs_count = make_all_independent_combs(file_name,
                                                 mitama_combs, expect_counts,
                                                 use_multi_process)

        print('Calculating finish, get %s independent combinations'
              % combs_count)


if __name__ == '__main__':
    multiprocessing.freeze_support()  # For windows platform

    try:
        main()
    except Exception:
        print(traceback.format_exc())
    finally:
        input('\nPress any key to exit')
