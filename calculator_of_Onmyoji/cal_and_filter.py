# coding: utf-8

import itertools

from calculator_of_Onmyoji import data_format


def make_combination(data_dict):
    if len(data_dict) != 6:
        raise KeyError("combination dict source must have 6 keys")

    d1, d2, d3, d4, d5, d6 = data_dict.values()
    return list(itertools.product(d1, d2, d3, d4, d5, d6))


def filter_mitama(mitama_comb_list, mitama_enhance, 
                  mitama_type='', type_min_num=0, 
                  prop_type='', prop_min_value=0):

    comb_data_list = cal_mitama_comb_prop(mitama_comb_list, mitama_enhance)
    
    filter_result = []
    for comb_data in comb_data_list:
        sum_data = comb_data.get('sum', {})
        if (mitama_type and 
                not fit_mitama_type(sum_data, mitama_type, type_min_num)):
            continue
        if (prop_type and
                not fit_prop_value(sum_data, prop_type, prop_min_value)):
            continue
        filter_result.append(comb_data)

    return filter_result


def fit_mitama_type(comb_sum_data, mitama_type, min_num):
    mitama_count = comb_sum_data.get(u'御魂计数', {}).get(mitama_type, 0)
    if mitama_count >= min_num:
        return True
    else:
        return False


def fit_prop_value(comb_sum_data, prop_type, min_value):
    prop_value = comb_sum_data.get(prop_type, 0)
    if prop_value >= min_value:
        return True
    else:
        return False


def cal_mitama_comb_prop(comb_list, mitama_enhance):
    mitama_comb_data = list()
    for comb in comb_list:
        comb_sum = sum_prop(comb, mitama_enhance)
        comb_data = {'sum': comb_sum,
                     'info': comb}
        mitama_comb_data.append(comb_data)

    return mitama_comb_data


def sum_prop(mitama_comb, mitama_enhance):
    prop_type_list = data_format.MITAMA_COL_NAME_ZH[3::]
    sum_result = {k: 0 for k in prop_type_list}
    mitama_type_count = {}
    for mitama in mitama_comb:
        mitama_info = mitama.values()[0]

        # 记录总御魂类型，用于计算御魂套装加成 
        mitama_type = mitama_info.get(u'御魂类型')
        if mitama_type not in mitama_type_count:
            mitama_type_count[mitama_type] = 1
        else:
            mitama_type_count[mitama_type] += 1

        # 计算除套装外的总属性
        for prop_type in prop_type_list:
            if mitama_info[prop_type]:
                sum_result[prop_type] += mitama_info[prop_type]

    for m_type, m_count in mitama_type_count.items():
        if m_count < 2:  # 忽略套装效果
            continue
        else:
            multi_times = 2 if m_count == 6 else 1  # 6个同类型御魂计算2次套装效果
            prop_type = mitama_enhance[m_type].get(u'加成类型')
            sum_result[prop_type] += multi_times * mitama_enhance[m_type].get(u'加成数值')

    sum_result[u'御魂计数'] = mitama_type_count

    return sum_result


if __name__ == '__main__':
    # test
    import load_data
    test_file = './example/data_Template.xlsx'
    d = load_data.get_mitama_data(test_file)
    l_d = load_data.sep_mitama_by_loc(d)
    m_e = load_data.get_mitama_enhance(test_file)

    comb = make_combination(l_d)
    print(len(comb))

    f_t = filter_mitama(comb, m_e, mitama_type=u'针女', type_min_num=4)
    print(len(f_t))

    f_p = filter_mitama(comb, m_e, prop_type=u'暴击', prop_min_value=90) 
    print(len(f_p))

    f_t_p = filter_mitama(comb, m_e, mitama_type=u'针女', type_min_num=4,
                          prop_type=u'暴击', prop_min_value=90)
    print(len(f_t_p))
