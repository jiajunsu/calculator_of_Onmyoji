# coding: utf-8

import string

import xlwt

import data_format


MAX_ROW = 60000


def write_mitama_result(filename, comb_data_list,
                        base_att=0, base_hp=0, base_critdamage=0):
    workbook = xlwt.Workbook(encoding='utf-8')
    result_num = 0
    result_sheet_num = 0
    detail_sheet_num = 0

    result_sheet = workbook.add_sheet('result_%s' % result_sheet_num)
    detail_sheet = workbook.add_sheet('detail_%s' % detail_sheet_num)
    result_sheet_num += 1
    detail_sheet_num += 1

    write_header_row(result_sheet, 'result')
    write_header_row(detail_sheet, 'detail')

    result_row = 1
    detail_row = 1
    serial_num = 1
    try:
        for comb_data in comb_data_list:
            if result_sheet_num > 2:
                print('Too many results, please enhance restrictive'
                      'condition.')
                break

            result_num += 1
            # first row of each comb_data is sum info
            sum_data = comb_data.get('sum', {})
            # first colume of a mitama_comb is serial number
            result_sheet.write(result_row, 0, label=serial_num)
            result_sheet.write(result_row, 2, label=u'sum')
            write_mitama_row(result_sheet, sum_data, result_row, start_col=4)
            write_extend_col(result_sheet, result_row, base_att, base_hp,
                             base_critdamage)
            result_row += 1
            if result_row > MAX_ROW:
                result_sheet = workbook.add_sheet(u'result_%s' % result_sheet_num)
                write_header_row(result_sheet, 'result')
                result_sheet_num += 1
                result_row = 1

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
            if detail_row > MAX_ROW:
                detail_sheet = workbook.add_sheet('detail_%s' % detail_sheet_num)
                write_header_row(detail_sheet, 'detail')
                detail_sheet_num += 1
                detail_row = 1

            serial_num += 1
    except KeyboardInterrupt:
        print('\nRecieve SIGINT, stop.')

    workbook.save(filename)
    print("We got %s results" % result_num)


def write_header_row(worksheet, sheet_type):
    if sheet_type == 'result':
        header_row = data_format.OUTPUT_HEADER + data_format.EXTEND_HEADER
    elif sheet_type == 'detail':
        header_row = data_format.OUTPUT_HEADER
    else:
        header_row = data_format.MITAMA_COL_NAME_ZH

    col_nums = len(header_row)
    for c in range(col_nums):
        worksheet.write(0, c, label=header_row[c])


def write_mitama_row(worksheet, comb_prop, row_num, start_col,
                     header_key=data_format.OUTPUT_HEADER):

    for col in range(start_col, len(header_key)):
        cell_data = comb_prop.get(header_key[col])
        worksheet.write(row_num, col, label=cell_data)


def write_extend_col(worksheet, row_num, base_att, base_hp, base_critdamage):
    start_col = len(data_format.OUTPUT_HEADER)
    str_row_num = str(row_num + 1)  # excel行名称编号比行号大1
    # TODO(victor): improve the code style
    # LIMIT: u'式神基础攻击', u'式神基础生命', u'式神基础暴伤',
    # u'总攻击', u'总生命',
    # u'攻击x暴伤', u'生命×暴伤'
    worksheet.write(row_num, start_col, label=base_att)
    worksheet.write(row_num, start_col+1, label=base_hp)
    worksheet.write(row_num, start_col+2, label=base_critdamage)

    # 总攻击 = 基础攻击 * (1 + 攻击加成/100) + 御魂攻击
    base_att_col_name = string.uppercase[start_col] + str_row_num
    att_enhance_col_name = 'F' + str_row_num
    mitama_att_col_name = 'E' + str_row_num
    formula_att = '%s*(1+%s/100)+%s' % (base_att_col_name,
                                        att_enhance_col_name,
                                        mitama_att_col_name)
    worksheet.write(row_num, start_col+3, xlwt.Formula(formula_att))

    # 总生命 = 基础生命 * (1 + 生命加成/100) + 御魂生命
    base_hp_col_name = string.uppercase[start_col+1] + str_row_num
    hp_enhance_col_name = 'L' + str_row_num
    mitama_hp_col_name = 'K' + str_row_num
    formula_hp = '%s*(1+%s/100)+%s' % (base_hp_col_name,
                                       hp_enhance_col_name,
                                       mitama_hp_col_name)
    worksheet.write(row_num, start_col+4, xlwt.Formula(formula_hp))

    # 攻击×暴伤 = 总攻击 * (基础暴伤+御魂暴伤)/100
    total_att_col_name = string.uppercase[start_col+3] + str_row_num
    base_crit_damage_col_name = string.uppercase[start_col+2] + str_row_num
    mitama_crit_damage_col_name = 'J' + str_row_num
    formula_att_crit = '%s*(%s+%s)/100' % (total_att_col_name,
                                           base_crit_damage_col_name,
                                           mitama_crit_damage_col_name)
    worksheet.write(row_num, start_col+5, xlwt.Formula(formula_att_crit))

    # 生命×暴伤 = 总生命 * (基础暴伤+御魂暴伤)/100
    total_hp_col_name = string.uppercase[start_col+4] + str_row_num
    formula_hp_crit = '%s*(%s+%s)/100' % (total_hp_col_name,
                                          base_crit_damage_col_name,
                                          mitama_crit_damage_col_name)
    worksheet.write(row_num, start_col+6, xlwt.Formula(formula_hp_crit))


def write_original_mitama_data(filename, data):
    workbook = xlwt.Workbook(encoding='utf-8')

    data_sheet = workbook.add_sheet(u'御魂')
    write_header_row(data_sheet, 'data')
    row = 1

    for serial, prop in data.iteritems():
        data_sheet.write(row, 0, label=serial)
        write_mitama_row(data_sheet, prop, row, 1,
                         header_key=data_format.MITAMA_COL_NAME_ZH)
        row += 1

    workbook.save(filename)
