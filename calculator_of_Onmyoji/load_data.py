# coding: utf-8

import json
import os
import traceback

import xlrd

from calculator_of_Onmyoji import data_format


def get_ext_files(file_ext):
    work_path = os.getcwd()
    ext_files = []

    for f in os.listdir(work_path):
        file_path = os.path.join(work_path, f)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_path)

            if file_extension == file_ext:
                ext_files.append(file_path)

    return ext_files


def _get_sheet_rows(filename, sheet_name, print_trace=True):
    if not os.path.exists(filename):
        raise IOError("File not exists %s" % filename)

    try:
        xls_book = xlrd.open_workbook(filename=filename)
        data_sheet = xls_book.sheet_by_name(sheet_name)
        return data_sheet.get_rows()
    except Exception:
        if print_trace:
            print(traceback.format_exc())
        raise


def get_mitama_data_json(filename, ignore_serial):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict) and 'data' in data:
        if isinstance(data['data'], list):
            return load_json_from_editor(data, ignore_serial)
        else:
            return load_json_from_yyx(data, ignore_serial)
    elif isinstance(data, list):
        return load_json_from_ocr_editor(data, ignore_serial)
    else:
        print('Unsupport format')
        raise TypeError


def load_json_from_ocr_editor(data, ignore_serial):
    '''从OCR录入器读取数据'''
    mitama_data = dict()
    PERCENT_PROP = ['攻击加成', '防御加成', '暴击', '暴击伤害',
                    '生命加成', '效果命中', '效果抵抗']

    data_version = 1
    if data[0] == "yuhun_ocr2.0":
        data_version = 2
        data.pop(0)

    serial = 0
    for d in data:
        if data_version < 2:
            serial += 1
        else:
            serial = d['御魂ID']

        if skip_serial(serial, ignore_serial):
            continue
        if d.get('御魂等级', 15) < 15:
            continue
        # 百分比类数据乘100
        for p in d:
            if p in PERCENT_PROP:
                d[p] *= 100
        mitama_data[serial] = d

    return mitama_data


def load_json_from_yyx(data, ignore_serial):
    '''从痒痒熊读取数据'''
    PROP_NAME_MAP = {'Hp': '生命', 'Defense': '防御', 'Attack': '攻击',
                     'HpRate': '生命加成', 'DefenseRate': '防御加成',
                     'AttackRate': '攻击加成', 'Speed': '速度', 'CritRate': '暴击',
                     'CritPower': '暴击伤害', 'EffectHitRate': '效果命中',
                     'EffectResistRate': '效果抵抗'}

    PERCENT_PROP = ['攻击加成', '防御加成', '暴击', '暴击伤害',
                    '生命加成', '效果命中', '效果抵抗']

    MITAMA_COL_MAP = {'御魂序号': 'id', '御魂类型': 'suit_id',
                      '位置': 'pos'}

    def mitama_json_to_dict(json_obj):
        serial = json_obj['id']
        if skip_serial(serial, ignore_serial) \
           or json_obj.get('level', 15) < 15:
            return None
        mitama = {}
        for col_name in data_format.MITAMA_COL_NAME_ZH[1:]:
            if col_name in MITAMA_COL_MAP:
                mitama[col_name] = json_obj[MITAMA_COL_MAP[col_name]]
            else:
                mitama[col_name] = 0

        mitama['御魂类型'] = data_format.SUIT_ID_TO_NAME.get(mitama['御魂类型'])
        mitama['位置'] += 1

        attr_list = [json_obj['base_attr']]
        attr_list.extend(json_obj['attrs'])
        if 'single_attrs' in json_obj:
            attr_list.extend(json_obj['single_attrs'])

        for prop in attr_list:
            prop_name = PROP_NAME_MAP.get(prop['type'], None)
            if prop_name in data_format.MITAMA_PROPS:
                if prop_name in PERCENT_PROP:
                    mitama[prop_name] += float(prop['value'])*100
                else:
                    mitama[prop_name] += float(prop['value'])

        return (serial, mitama)

    mitama_list = map(mitama_json_to_dict, data['data'].get('hero_equips', []))
    return dict([x for x in mitama_list if x])


def load_json_from_editor(data, ignore_serial):
    '''从网页版御魂编辑器读取数据'''
    def mitama_json_to_dict(json_obj):
        MITAMA_COL_MAP = {'御魂序号': 'id', '御魂类型': 'name',
                          '位置': 'pos'}
        serial = json_obj['id']
        if skip_serial(serial, ignore_serial):
            return None
        mitama = {}
        for col_name in data_format.MITAMA_COL_NAME_ZH[1:]:
            if col_name in MITAMA_COL_MAP:
                mitama[col_name] = json_obj[MITAMA_COL_MAP[col_name]]
            else:
                mitama[col_name] = 0

        for props in [json_obj['mainAttr'],
                      json_obj['addonAttr']] + json_obj['addiAttr']:
            if props['attrName'] in data_format.MITAMA_PROPS:
                mitama[props['attrName']] += float(props['attrVal'])

        return (serial, mitama)

    mitama_list = map(mitama_json_to_dict, data['data'])
    return dict([x for x in mitama_list if x])


def get_ignore_serial_xls(filename):
    '''Load ignore serial from data xls'''
    ignore_serial = []
    try:
        rows_data = _get_sheet_rows(filename, '已使用',
                                    print_trace=False)
    except xlrd.biffh.XLRDError:
        return ignore_serial

    next(rows_data)
    for r_data in rows_data:
        serial = str(convert_int(r_data[1].value))
        if serial not in ignore_serial:
            ignore_serial.append(serial)

    return ignore_serial


def convert_int(s):
    '''Convert s to int or just return if failed'''
    try:
        s = int(s)
    except ValueError:
        pass
    return s


def get_mitama_data_xls(filename, ignore_serial):
    ignore_serial.extend(get_ignore_serial_xls(filename))
    rows_data = _get_sheet_rows(filename, '御魂')
    mitama_data = dict()
    data_len = len(data_format.MITAMA_COL_NAME_ZH)

    next(rows_data)  # skip first row
    for r_data in rows_data:
        serial = convert_int(r_data[0].value)
        if skip_serial(serial, ignore_serial):
            continue

        data = {data_format.MITAMA_COL_NAME_ZH[1]: r_data[1].value}

        for i in range(2, data_len):
            prop_name = data_format.MITAMA_COL_NAME_ZH[i]
            data[prop_name] = float(r_data[i].value) if r_data[i].value else 0

        if serial in mitama_data:
            print('Mitama serial must be unique %s' % serial)
            raise ValueError
        mitama_data.setdefault(serial, data)

    return mitama_data


def get_mitama_data(filename, ignore_serial):
    ext_name = os.path.splitext(filename)[1]
    if ext_name == '.xls':
        return get_mitama_data_xls(filename, ignore_serial)
    elif ext_name == '.json':
        return get_mitama_data_json(filename, ignore_serial)
    else:
        print("Unsupported file type!")

    return dict()


def skip_serial(serial, ignore_list):
    if not ignore_list:
        return False

    serial = str(serial)
    for ig in ignore_list:
        if not ig:
            continue
        if ig.isdigit():
            if ig == serial:
                # pure digit number as serial must be equal
                return True
        elif ig in serial:
            return True
    return False


def sep_mitama_by_loc(mitama_data):
    mitama_loc_data = {1: [], 2: [], 3: [],
                       4: [], 5: [], 6: []}

    for d_k, d_v in mitama_data.items():
        loc = d_v['位置']
        if loc not in mitama_loc_data:
            print('Mitama location must be 1 to 6, please check your data.')
        mitama_loc_data[loc].append({d_k: d_v})

    return mitama_loc_data


if __name__ == '__main__':
    # for test
    test_file = './example/data_Template.xls'
    d = get_mitama_data(test_file, [])
    print(d)
    l_d = sep_mitama_by_loc(d)
    print(l_d)

    from calculator_of_Onmyoji import write_data
    write_data.write_original_mitama_data('test.xls', d)
