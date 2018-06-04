# coding: utf-8

import xlwt


def write_data(filename, sheetname, datainfo):
    workbook = xlwt.Workbook(encoding='unicode')
    worksheet = workbook.add_sheet(sheetname)
