# coding: utf-8

import xlwt

import data_format


def write_mitama_result(filename, comb_data_list,
                        header_row=data_format.OUTPUT_HEADER):
    workbook = xlwt.Workbook(encoding='utf-8')
    result_sheet = workbook.add_sheet(u'result')
    detail_sheet = workbook.add_sheet(u'detail')

    col_nums = len(header_row)

    # write header row
    for c in range(col_nums):
        result_sheet.write(0, c, label=header_row[c])
        detail_sheet.write(0, c, label=header_row[c])

    result_row = 1
    detail_row = 1
    serial_num = 1
    for comb_data in comb_data_list:
        # first row of each comb_data is sum info
        sum_data = comb_data.get('sum', {})
        # first colume of a mitama_comb is serial number
        result_sheet.write(result_row, 0, label=serial_num)
        result_sheet.write(result_row, 2, label=u'sum')
        write_mitama_row(result_sheet, sum_data, result_row, start_col=4)
        result_row += 1

        # write each mitama data into detail file
        mitama_data = comb_data.get('info', set())
        for mitama in mitama_data:
            mitama_serial = mitama.keys()[0]
            mitama_prop = mitama[mitama_serial]
            detail_sheet.write(detail_row, 0, label=serial_num)
            detail_sheet.write(detail_row, 1, label=mitama_serial)
            write_mitama_row(detail_sheet, mitama_prop,
                             detail_row, start_col=2)
            detail_row += 1

        serial_num += 1

    workbook.save(filename)


def write_mitama_row(worksheet, comb_prop, row_num, start_col,
                     header_key=data_format.OUTPUT_HEADER):

    for col in range(start_col, len(header_key)):
        cell_data = comb_prop.get(header_key[col])
        worksheet.write(row_num, col, label=cell_data)
