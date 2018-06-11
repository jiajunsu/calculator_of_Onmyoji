# coding: utf-8

import itertools

from calculator_of_Onmyoji import data_format


def make_combination(data_dict):
    if len(data_dict) != 6:
        raise KeyError("combination dict source must have 6 keys")

    d1, d2, d3, d4, d5, d6 = data_dict.values()
    print('mitama nums by loc is %s %s %s %s %s %s' % (len(d1), len(d2),
                                                       len(d3), len(d4),
                                                       len(d5), len(d6)))
    return itertools.product(d1, d2, d3, d4, d5, d6)


def filter_loc_prop(data_list, prop_type, prop_min_value):
    def prop_value_le_min(mitama):
        mitama_info = mitama.values()[0]
        if (mitama_info[prop_type] and
                mitama_info[prop_type] >= prop_min_value:)
            return True
        else:
            return False

    return filter(prop_value_le_min, data_list)


def filter_mitama(mitama_comb_list, mitama_enhance,
                  mitama_type='', type_min_num=0,
                  prop_type='', prop_min_value=0):

    mitama_sum_data = fit_mitama_type(mitama_comb_list,
                                      mitama_type, type_min_num)
    print('filter mitama type finish')

    if prop_type:
        mitama_sum_data = fit_prop_value(mitama_sum_data, prop_type,
                                         prop_min_value, mitama_enhance)
    print('filter mitama prop value finish')

    comb_data_list = cal_mitama_comb_prop(mitama_sum_data, mitama_enhance)
    print('cal mitama sum prop finish')

    return comb_data_list


def fit_mitama_type(mitama_comb_list, expect_mitama_type, min_num):
    for mitama_comb in mitama_comb_list:
        mitama_type_count = {}
        for mitama in mitama_comb:
            mitama_info = mitama.values()[0]

            mitama_type = mitama_info.get(u'御魂类型')
            if mitama_type not in mitama_type_count:
                mitama_type_count[mitama_type] = 1
            else:
                mitama_type_count[mitama_type] += 1

        if (not expect_mitama_type) or (expect_mitama_type
                and mitama_type_count.get(expect_mitama_type) >= min_num):
            comb_data = {'sum': {u'御魂计数': mitama_type_count},
                         'info': mitama_comb}
            yield comb_data


def fit_prop_value(mitama_sum_data, prop_type, min_value, mitama_enhance):
    for mitama_data in mitama_sum_data:
        mitama_type_count = mitama_data['sum'].get(u'御魂计数')
        mitama_comb = mitama_data['info']
        prop_value = 0

        for mitama in mitama_comb:
            mitama_info = mitama.values()[0]
            if mitama_info[prop_type]:
                prop_value += mitama_info[prop_type]

        for m_type, m_count in mitama_type_count.items():
            if m_count < 2:
                continue
            else:
                p_type = mitama_enhance[m_type].get(u'加成类型')
                if p_type == prop_type:
                    multi_times = 2 if m_count == 6 else 1  # 6个御魂算2次套装
                    prop_value += (
                        multi_times * mitama_enhance[m_type].get(u'加成数值'))

        if prop_value >= min_value:
            yield mitama_data


def cal_mitama_comb_prop(mitama_sum_data, mitama_enhance):
    for mitama_data in mitama_sum_data:
        mitama_type_count = mitama_data['sum'].get(u'御魂计数')
        mitama_comb = mitama_data['info']

        comb_sum = sum_prop(mitama_comb, mitama_type_count, mitama_enhance)

        comb_data = {'sum': comb_sum,
                     'info': mitama_comb}
        yield comb_data


def sum_prop(mitama_comb, mitama_type_count, mitama_enhance):
    prop_type_list = data_format.MITAMA_COL_NAME_ZH[3::]
    sum_result = {k: 0 for k in prop_type_list}

    for mitama in mitama_comb:
        mitama_info = mitama.values()[0]

        # 计算除套装外的总属性
        for prop_type in prop_type_list:
            if mitama_info[prop_type]:
                sum_result[prop_type] += mitama_info[prop_type]

    for m_type, m_count in mitama_type_count.items():
        if m_count < 2:  # 忽略套装效果
            continue
        else:
            multi_times = 2 if m_count == 6 else 1  # 6个同类御魂算2次套装效果
            prop_type = mitama_enhance[m_type].get(u'加成类型')
            if prop_type:
                sum_result[prop_type] += (
                        multi_times * mitama_enhance[m_type].get(u'加成数值'))

    return sum_result


if __name__ == '__main__':
    # test
    import load_data
    test_file = './example/data_Template.xls'
    d = load_data.get_mitama_data(test_file)
    l_d = load_data.sep_mitama_by_loc(d)
    m_e = load_data.get_mitama_enhance(test_file)

    comb = make_combination(l_d)
    f_t = filter_mitama(comb, m_e, mitama_type=u'针女', type_min_num=4)
    print(len(list(f_t)))

    comb = make_combination(l_d)
    f_p = filter_mitama(comb, m_e, prop_type=u'暴击', prop_min_value=90)
    print(len(list(f_p)))

    comb = make_combination(l_d)
    f_t_p = filter_mitama(comb, m_e, mitama_type=u'针女', type_min_num=4,
                          prop_type=u'暴击', prop_min_value=90)
    print(len(list(f_t_p)))
