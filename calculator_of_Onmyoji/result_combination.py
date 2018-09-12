#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt



def load_result(filename):
    xls_book = xlrd.open_workbook(filename=filename)
    data_sheet = xls_book.sheet_by_name('result')

    rows_data = data_sheet.get_rows()

    # TODO: deserialize data into list



if __name__ == '__main__':
    pass
