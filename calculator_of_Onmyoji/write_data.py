# coding: utf-8

import xlwt

from calculator_of_Onmyoji import data_format


MAX_ROW = 65532  # divided by 6 for each result is a combination of 6 details


def write_mitama_result(filename, comb_data_list, es_prop,
                        base_att=0, base_hp=0, base_critdamage=0):
    workbook = xlwt.Workbook(encoding='utf-8')
    result_num = 0
    detail_sheet_num = 0

    result_sheet = workbook.add_sheet('result')
    detail_sheet = workbook.add_sheet('detail_%s' % detail_sheet_num)
    detail_sheet_num += 1

    write_header_row(result_sheet, 'result')
    write_header_row(detail_sheet, 'detail')

    es_col = data_format.RESULT_HEADER_LEN

    if es_prop:
        detail_sheet.write(0, es_col, label='极品度')

    result_row = 1
    detail_row = 1
    serial_num = 1
    try:
        for comb_data in comb_data_list:
            if result_row > MAX_ROW:
                print('Too many results, please enhance restrictive'
                      'condition.')
                break

            result_num += 1
            # first row of each comb_data is sum info
            sum_data = comb_data.get('sum', {})
            # first colume of a mitama_comb is serial number
            result_sheet.write(result_row, 0, label=serial_num)
            result_sheet.write(result_row, 2, label='sum')
            write_mitama_row(result_sheet, sum_data, result_row, start_col=4)
            write_extend_col(result_sheet, result_row, base_att, base_hp,
                             base_critdamage)
            result_row += 1

            # write each mitama data into detail file
            mitama_data = comb_data.get('info', set())
            serial_keys = []
            for mitama in mitama_data:
                mitama_serial = list(mitama.keys())[0]
                serial_keys.append(str(mitama_serial))
                mitama_prop = mitama[mitama_serial]
                detail_sheet.write(detail_row, 0, label=serial_num)
                detail_sheet.write(detail_row, 1, label=mitama_serial)
                write_mitama_row(detail_sheet, mitama_prop,
                                 detail_row, start_col=2)

                if es_prop:
                    prop_num = cal_es_prop_num(mitama_prop, es_prop)
                    detail_sheet.write(detail_row, es_col, label=prop_num)

                detail_row += 1

            # mimata serial in result sheet is the comb of mitama_data serials
            str_serial_keys = ','.join(serial_keys)
            result_sheet.write(result_row-1, 1, label=str_serial_keys)

            if detail_row > MAX_ROW:
                detail_sheet = workbook.add_sheet('detail_%s'
                                                  % detail_sheet_num)
                write_header_row(detail_sheet, 'detail')
                detail_sheet_num += 1
                detail_row = 1

            serial_num += 1
    except KeyboardInterrupt:
        print('\nRecieve SIGINT, stop.')

    workbook.save(filename)
    print("We got %s results" % result_num)

    return result_num


def write_header_row(worksheet, sheet_type):
    if sheet_type == 'result':
        header_row = data_format.RESULT_HEADER + data_format.EXTEND_HEADER
    elif sheet_type == 'detail':
        header_row = data_format.RESULT_HEADER
    elif sheet_type == 'result_combs':
        header_row = data_format.RESULT_COMB_HEADER
    elif sheet_type == 'data_with_esp':
        header_row = (data_format.MITAMA_COL_NAME_ZH +
                      data_format.MITAMA_ESP_EXTEND_HEADER)
    else:
        header_row = data_format.MITAMA_COL_NAME_ZH

    col_nums = len(header_row)
    for c in range(col_nums):
        worksheet.write(0, c, label=header_row[c])


def write_mitama_row(worksheet, comb_prop, row_num, start_col,
                     header_key=data_format.RESULT_HEADER):

    for col in range(start_col, len(header_key)):
        cell_data = comb_prop.get(header_key[col])
        worksheet.write(row_num, col, label=cell_data)


def write_extend_col(worksheet, row_num, base_att, base_hp, base_critdamage):
    start_col = data_format.RESULT_HEADER_LEN
    str_row_num = str(row_num + 1)  # excel行名称编号比行号大1
    # EXTEND_COL: u'式神基础攻击', u'式神基础生命', u'式神基础暴伤',
    # u'总攻击', u'总生命',
    # u'攻击x暴伤', u'生命×暴伤'
    worksheet.write(row_num, start_col, label=base_att)
    worksheet.write(row_num, start_col+1, label=base_hp)
    worksheet.write(row_num, start_col+2, label=base_critdamage)

    # 总攻击 = 基础攻击 * (1 + 攻击加成/100) + 御魂攻击
    base_att_col_name = data_format.EXTEND_INDEX['式神基础攻击'] + str_row_num
    att_enhance_col_name = data_format.RESULT_INDEX['攻击加成'] + str_row_num
    mitama_att_col_name = data_format.RESULT_INDEX['攻击'] + str_row_num
    formula_att = '%s*(1+%s/100)+%s' % (base_att_col_name,
                                        att_enhance_col_name,
                                        mitama_att_col_name)
    worksheet.write(row_num, start_col+3, xlwt.Formula(formula_att))

    # 总生命 = 基础生命 * (1 + 生命加成/100) + 御魂生命
    base_hp_col_name = data_format.EXTEND_INDEX['式神基础生命'] + str_row_num
    hp_enhance_col_name = data_format.RESULT_INDEX['生命加成'] + str_row_num
    mitama_hp_col_name = data_format.RESULT_INDEX['生命'] + str_row_num
    formula_hp = '%s*(1+%s/100)+%s' % (base_hp_col_name,
                                       hp_enhance_col_name,
                                       mitama_hp_col_name)
    worksheet.write(row_num, start_col+4, xlwt.Formula(formula_hp))

    # 攻击×暴伤 = 总攻击 * (基础暴伤+御魂暴伤)/100
    total_att_col_name = data_format.EXTEND_INDEX['总攻击'] + str_row_num
    base_crit_damage_col_name = (data_format.EXTEND_INDEX['式神基础暴伤'] +
                                 str_row_num)
    mitama_crit_damage_col_name = (data_format.RESULT_INDEX['暴击伤害'] +
                                   str_row_num)
    formula_att_crit = '%s*(%s+%s)/100' % (total_att_col_name,
                                           base_crit_damage_col_name,
                                           mitama_crit_damage_col_name)
    worksheet.write(row_num, start_col+5, xlwt.Formula(formula_att_crit))

    # 生命×暴伤 = 总生命 * (基础暴伤+御魂暴伤)/100
    total_hp_col_name = data_format.EXTEND_INDEX['总生命'] + str_row_num
    formula_hp_crit = '%s*(%s+%s)/100' % (total_hp_col_name,
                                          base_crit_damage_col_name,
                                          mitama_crit_damage_col_name)
    worksheet.write(row_num, start_col+6, xlwt.Formula(formula_hp_crit))


def write_original_mitama_data(filename, data, esps_show=False):
    workbook = xlwt.Workbook(encoding='utf-8')

    data_sheet = workbook.add_sheet('御魂')
    if esps_show:
        write_header_row(data_sheet, 'data_with_esp')
    else:
        write_header_row(data_sheet, 'data')

    row = 1

    for serial, prop in data.items():
        data_sheet.write(row, 0, label=serial)
        write_mitama_row(data_sheet, prop, row, 1,
                         header_key=data_format.MITAMA_COL_NAME_ZH)

        col_esp_extend = len(data_format.MITAMA_COL_NAME_ZH)
        if esps_show:
            for esp_main in data_format.MITAMA_ESP_EXTEND_HEADER:
                es_prop = data_format.MITAMA_ESP[esp_main]
                prop_num = cal_es_prop_num(prop, es_prop)
                data_sheet.write(row, col_esp_extend, label=prop_num)
                col_esp_extend += 1

        row += 1

    ignore_sheet = workbook.add_sheet('已使用')
    write_header_row(ignore_sheet, 'detail')

    workbook.save(filename)


def cal_es_prop_num(mitama_prop, effect_second_prop):
    mitama_growth = data_format.MITAMA_GROWTH
    prop_num = 0
    for select_prop in effect_second_prop:
        prop_value = mitama_prop.get(select_prop, 0.0)
        main_prop_value = mitama_growth[select_prop]["主属性"]
        max_prop_value = mitama_growth[select_prop]["副属性最大值"]
        if prop_value >= max_prop_value:
            prop_value -= main_prop_value
        prop_num += prop_value / mitama_growth[select_prop]["最小成长值"]

    if prop_num < 0:
        prop_num = 0

    return prop_num
