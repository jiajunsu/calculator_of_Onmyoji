#!/usr/bin/env python
# -*- coding:utf-8 -*-

from itertools import combinations
from collections import defaultdict
import locale
from math import factorial
import multiprocessing
import os
import traceback

from tqdm import tqdm
import xlrd
import xlwt
from xlutils.copy import copy

from calculator_of_Onmyoji import data_format
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


code_t = locale.getpreferredencoding()


class ResultBook(object):
    def __init__(self, filename, postfix):
        self.filename = filename
        self.postfix = str(postfix)

        # read_book = xlrd.open_workbook(filename=self.filename)
        # self.write_book = copy(read_book)
        self.write_book = xlwt.Workbook(encoding='utf-8')

        self.work_sheet = None
        self.work_sheet_num = 0
        self.row_num = 0
        self.count = 0

    def init_work_sheet(self):
        self.work_sheet = self.write_book.add_sheet(u'independent_combs_%s'
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
        for res_book in self.result_book.itervalues():
            res_book.save()

    @property
    def count(self):
        count = 0
        for res_book in self.result_book.itervalues():
            count += res_book.count
        return count


def load_result_sheet(filename):
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


def get_independent_comb_data(mitama_combs):
    seed_serials = set()

    for combs_data in mitama_combs:
        # print(combs_data)
        mitama_serials = combs_data.get(u'御魂序号') # set(123456)
        if seed_serials & mitama_serials:
            return None
        else:
            seed_serials |= mitama_serials

    return gen_result_comb_data(mitama_combs)


def make_independent_comb(file_name, mitama_combs, last_result_combs, sub_comb_length, cores, allMitamaSet, invertMitamaSet):
    '''遍历组合，找出独立组合并触发写数据'''
    n = len(mitama_combs)
    # total = cal_comb_num(n, sub_comb_length)
    total = 0
    # print('Calculating C(%s, %s) = %s' % (n, sub_comb_length, total))

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
        print("Loading mitamas...")
        result_book = ResultBook(file_name, sub_comb_length)
        mitama_combs_next = []

        print('Calculating %d combo results...' %sub_comb_length)

        if sub_comb_length==2:
            for midx in tqdm(xrange(len(mitama_combs)),
                              desc='Calculating', total=n, unit='comb'):
                comb = mitama_combs[midx]
                mitama_serials = comb.get(u'御魂序号')
                available_combs = reduce(lambda x,y:x-y, [allMitamaSet]+[invertMitamaSet[ms] for ms in mitama_serials])

                for ac in available_combs:
                    if ac>midx:
                        # pass
                        comb_data = gen_result_comb_data([comb, mitama_combs[ac]])
                        # mitama_combs_next.append(comb_data)
                        # print(comb_data)
                        # result_book.write(comb_data)
        else:
            for midx in tqdm(xrange(len(last_result_combs)),
                              desc='Calculating', total=n, unit='comb'):
                rcomb = last_result_combs[midx]
                last_comb_serials = rcomb.get(u'组合序号').split(',')
                comb = [mitama_combs[int(i)-1] for i in last_comb_serials]
                mitama_serials = reduce(lambda x,y:x|y, map(lambda x:x.get(u'御魂序号'), comb))
                # print(mitama_serials)
                available_combs = reduce(lambda x,y:x-y, [allMitamaSet]+[invertMitamaSet[ms] for ms in mitama_serials])
                # print('available_combs')
                # print(available_combs)

                max_idx = int(max(last_comb_serials))-1
                # print(max_idx)
                for ac in available_combs:
                    if ac>max_idx:
                        # pass
                        comb_data = gen_result_comb_data(comb + [mitama_combs[ac]])
                        # mitama_combs_next.append(comb_data)
                        # print(comb_data)
                        # result_book.write(comb_data)

        # print("Writing results...")
        # for comb_data in tqdm(mitama_combs_next, 
        #                     desc='Writing', total=len(mitama_combs_next), unit='comb'):
        #     result_book.write(comb_data)

        result_book.save()
        return result_book.count, mitama_combs_next


def cal_comb_num(n, m):
    '''计算组合数

    C(n, m) = n!/((n-m)! * m!)
    '''
    x = 1
    for i in xrange(n, m, -1):
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
        for c in xrange(2, len(mitama_combs)):
            # 从2开始遍历，直至无法再找到独立组合
            res_count = make_independent_comb(file_name,
                                              mitama_combs, c, cores)
            if res_count == 0:
                break
            combs_count += res_count
    else:
        invertMitamaSet = defaultdict(set)
        allMitamaSet = set()
        for midx in tqdm(xrange(len(mitama_combs)), desc='Initializing', total=len(mitama_combs), unit='comb'):
            mitama_comb = mitama_combs[midx]
            mitama_serials = mitama_comb.get(u'御魂序号') # set(123456)
            for mitama in mitama_serials:
                invertMitamaSet[mitama] |= set([midx])
                allMitamaSet |= set([midx])
        # print(invertMitamaSet)
        combs_count = 0
        result_combs = []
        for expect in xrange(2,expect_counts+1):
            # print(expect)
            # print(result_combs)
            combs_count,result_combs = make_independent_comb(file_name,
                                            mitama_combs, result_combs, expect, cores, allMitamaSet, invertMitamaSet)
            if combs_count==0:
                break

    return combs_count


def merge(A, B, f):
    """merge two dict; py2 style"""
    # Start with symmetric difference; keys either in A or B, but not both
    merged = {k: A.get(k, B.get(k)) for k in A.viewkeys() ^ B.viewkeys()}
    # Update with `f()` applied to the intersection
    merged.update({k: f(A[k], B[k]) for k in A.viewkeys() & B.viewkeys()})
    return merged

def merge_func(a, b):
    return ','.join([str(a),str(b)])

def gen_result_comb_data(independent_comb):
    # A = {k:independent_comb[0][k] for k in data_format.RESULT_COMB_HEADER[1:] if k in independent_comb[0]}
    # B = {k:independent_comb[1][k] for k in data_format.RESULT_COMB_HEADER[1:] if k in independent_comb[1]}
    # result_comb_data = merge(A,B, merge_func)
    # result_comb_data[u'组合个数'] = len(independent_comb)

    result_comb_data = {key:','.join([str(d[key]) for d in independent_comb]) 
                            for key in data_format.RESULT_COMB_HEADER[1:]}
    result_comb_data[u'组合个数'] = len(independent_comb)
    # result_comb_data = {u'组合个数': len(independent_comb)}


    # for key in data_format.RESULT_COMB_HEADER[1:]:
    #     ## result_comb_data[key] = ','.join([str(d.get(key, 0))
    #     ##                                   for d in independent_comb])
    #     result_comb_data[key] = ','.join([str(d[key])
    #                                       for d in independent_comb])
    #     # result_comb_data[key] = reduce(lambda x,y:x+','+y, [str(d[key])
    #     #                                   for d in independent_comb])

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
        pass
        # raw_input('\nPress any key to exit')