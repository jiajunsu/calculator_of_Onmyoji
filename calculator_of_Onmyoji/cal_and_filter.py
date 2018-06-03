# coding: utf-8

import itertools

import data_format


def make_combination(data_dict):
    if len(data_dict) != 6:
        raise KeyError("combination dict source must have 6 keys")

    d1, d2, d3, d4, d5, d6 = data_dict.values()
    return list(itertools.product(d1, d2, d3, d4, d5, d6))


def filter_by_mitama_type(comb_list, mitama_type, min_num):
    filter_result = []
    for comb in comb_list:
        count = 0
        for mitama in comb:
            mitama_info = mitama.values()[0]
            if mitama_info.get(u'御魂类型') == mitama_type:
                count += 1
        if count >= min_num:
            filter_result.append(comb)

    return filter_result


def filter_by_prop_value(comb_list, prop_type, min_value, mitama_enhance):
    filter_result = []
    for comb in comb_list:
        mitama_type_count = {}
        prop_value = 0
        for mitama in comb:
            mitama_info = mitama.values()[0]
            # 指定属性值求和
            if mitama_info.get(prop_type):
                prop_value += mitama_info.get(prop_type)
            # 记录总御魂类型，用于下面计算御魂套装加成 
            mitama_type = mitama_info.get(u'御魂类型')
            if mitama_type not in mitama_type_count:
                mitama_type_count[mitama_type] = 1
            else:
                mitama_type_count[mitama_type] += 1
        for m_type, m_count in mitama_type_count.items():
            if mitama_enhance[m_type].get(u'加成类型') != prop_type:
                # 套装效果不属于过滤条件
                continue
            if m_count < 2:  # 忽略套装效果
                continue
            elif 2 <= m_count <= 5:  # 计算一次套装效果
                prop_value += mitama_enhance[m_type].get(u'加成数值')
            elif m_count == 6:  # 计算两次套装效果
                prop_value += 2 * mitama_enhance[m_type].get(u'加成数值')

        if prop_value >= min_value:
            filter_result.append(comb)

    return filter_result


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

    return sum_result


if __name__ == '__main__':
    # test
    import load_data
    test_file = './example/data_Template.xlsx'
    d = load_data.get_mitama_data(test_file)
    l_d = load_data.sep_mitama_by_loc(d)

    comb = make_combination(l_d)
    print(len(comb))

    f_r = filter_by_mitama_type(comb, u'针女', 4)
    print(len(f_r))

    m_e = load_data.get_mitama_enhance(test_file)
    f_p_r = filter_by_prop_value(comb, u'暴击', 90, m_e) 
    print(len(f_p_r))
