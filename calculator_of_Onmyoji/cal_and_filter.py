# coding: utf-8

import itertools
import sys

from calculator_of_Onmyoji import data_format


def filter_loc_and_type(data_dict,
                        l2_prop_limit,
                        l4_prop_limit,
                        l6_prop_limit,
                        attack_only,
                        es_prop,
                        es_prop_num):
    if len(data_dict) != 6:
        raise KeyError("combination dict source must have 6 keys")

    print('mitama nums by loc is %s'
          % str([len(d) for d in data_dict.values()]))

    if attack_only:
        # 只计算输出类御魂
        for loc, data in data_dict.iteritems():
            data_dict[loc] = filter_mitama_type(data,
                                                data_format.ATTACK_MITAMA_TYPE)

    # 246号位主属性过滤
    if l2_prop_limit:
        data_dict[2] = filter_loc_prop(data_dict[2], l2_prop_limit)
    if l4_prop_limit:
        data_dict[4] = filter_loc_prop(data_dict[4], l4_prop_limit)
    if l6_prop_limit:
        data_dict[6] = filter_loc_prop(data_dict[6], l6_prop_limit)

    # 全位置副属性过滤
    if es_prop and es_prop_num:
        for loc, data_list in data_dict.iteritems():
            data_dict[loc] = \
                filter_effective_secondary_prop(data_list,
                                                es_prop,
                                                es_prop_num[loc-1])

    print('after filter by loc prop and type %s'
          % str([len(d) for d in data_dict.values()]))

    return dict(zip(range(1, 7), [d for d in data_dict.values()]))


def find_mtype_candidates(mitama_type='ALL'):
    candidates = []
    if mitama_type == 'ALL':
        candidates = data_format.MITAMA_TYPES
    elif mitama_type in data_format.MITAMA_TYPES:
        candidates.append(mitama_type)
    elif mitama_type in data_format.MITAMA_PROPS:
        for m_type in data_format.MITAMA_TYPES:
            if data_format.MITAMA_ENHANCE[m_type][u"加成类型"] == mitama_type:
                candidates.append(m_type)
    return candidates


def gen_mitama_combos(mitama_type_limit=None, all_suit=True):
    if mitama_type_limit is None:
        mitama_type_limit = []
    main_type, secondary_type = None, []
    fixed_pos = 0
    for m_type, limit_count in mitama_type_limit:
        if m_type not in data_format.MITAMA_TYPES and\
           m_type not in data_format.MITAMA_PROPS:
            continue
        if limit_count == 4:
            main_type = m_type
            fixed_pos += 4
        elif limit_count == 2:
            secondary_type.append(m_type)
            fixed_pos += 2

    if main_type is not None:
        main_candidates = find_mtype_candidates(main_type)
        if fixed_pos == 6 or all_suit:  # 4+2
            if secondary_type:
                secondary_candidates = find_mtype_candidates(secondary_type[0])
            elif all_suit:
                secondary_candidates = find_mtype_candidates()
            for m_type in main_candidates:
                for s_type in secondary_candidates:
                    yield [m_type] * 4 + [s_type] * 2
        else:       # 4+1+1
            yield [m_type] * 4 + ['ALL', 'ALL']

    elif fixed_pos == 6 or (all_suit and fixed_pos >= 2):    # 2+2+2, 2+2+any, 2+any+any
        candidates = []
        for m_type in secondary_type:
            candidates.append(find_mtype_candidates(m_type))
        for i in range((6-fixed_pos)//2):
            candidates.append(find_mtype_candidates())
        generated = {}
        for t1, t2, t3 in itertools.product(*candidates):
            if frozenset((t1, t2, t3)) not in generated and\
               t1 != t2 and t2 != t3 and t1 != t3:
                generated[frozenset((t1, t2, t3))] = True
                yield [t1, t2, t3]*2
    elif fixed_pos >= 2:
        candidates = []
        for m_type in secondary_type:
            candidates.append(find_mtype_candidates(m_type))

        for i in range(6-fixed_pos):
            candidates.append(["ALL"])
        generated = {}
        for combo in itertools.product(*candidates):
            if len(set(combo[:fixed_pos//2])) != fixed_pos//2:
                continue
            t1, t2, t3, t4, t5, t6 = combo[:fixed_pos//2]*2 + combo[fixed_pos//2:]
            if frozenset((t1, t2, t3, t4, t5, t6)) not in generated:
                generated[frozenset((t1, t2, t3, t4, t5, t6))] = True
                yield [t1, t2, t3, t4, t5, t6]
    else:
        yield None


def gen_mitama_permutations(mitama_type_limit=None, all_suit=True):
    if mitama_type_limit is None:
        mitama_type_limit = []
    generated = {}
    for m_combos in gen_mitama_combos(mitama_type_limit, all_suit):
        if m_combos is None:
            yield None
        else:
            print(",".join(m_combos))
            for m_permu in itertools.permutations(m_combos):
                if tuple(m_permu) not in generated:
                    generated[tuple(m_permu)] = True
                    yield m_permu


def make_combination(mitama_data, mitama_type_limit=None, all_suit=True):
    if mitama_type_limit is None:
        mitama_type_limit = []
    main_type, secondary_type = None, None
    total_comb = 0

    def filter_mitama_by_type(mitama, desired_type):
        mitama_info = mitama.values()[0]
        if (mitama_info[u'御魂类型'] == desired_type):
            return True
        else:
            return False

    def classify_by_type():
        mitama_data_by_type = {}
        for m_type in data_format.MITAMA_TYPES:
            mitama_data_by_type[m_type] = {}
            for i in range(1, 7):
                mitama_data_by_type[m_type][i] =\
                    filter(lambda x: filter_mitama_by_type(x, m_type),
                           mitama_data[i])
        return mitama_data_by_type

    mitama_data_by_type = None
    res = []
    for m_combos in gen_mitama_permutations(mitama_type_limit, all_suit):
        if m_combos is None:
            total_comb = reduce(lambda x, y: x*y,
                                map(len, mitama_data.values()))
            print("Total combinations: {}".format(total_comb))
            return itertools.product(*mitama_data.values()), total_comb
        else:
            if mitama_data_by_type is None:
                mitama_data_by_type = classify_by_type()
            mitama_grp = {x: mitama_data[x] if m_type == 'ALL' else mitama_data_by_type[m_type][x]
                          for x, m_type in zip(range(1, 7), m_combos)}
            total_comb += reduce(lambda x, y: x*y,
                                 map(len, mitama_grp.values()))
            res.append(itertools.product(*mitama_grp.values()))

    print("Total combinations: {}".format(total_comb))
    return itertools.chain(*res), total_comb


def filter_loc_prop(data_list, prop_limit):
    def prop_value_le_min(mitama):
        mitama_info = mitama.values()[0]
        for prop_type, prop_min_value in prop_limit.items():
            if (mitama_info.get(prop_type, 0) and
                    mitama_info[prop_type] >= prop_min_value):
                return True
        else:
            return False

    return filter(prop_value_le_min, data_list)


def filter_effective_secondary_prop(data_list, es_prop, es_prop_num):
    mitama_growth = data_format.MITAMA_GROWTH

    def es_prop_num_le_min(mitama):
        mitama_info = mitama.values()[0]
        prop_num = 0
        for prop in es_prop:
            prop_value = mitama_info.get(prop, 0.0)
            main_prop_value = mitama_growth[prop][u"主属性"]
            if prop_value >= main_prop_value:
                prop_value -= main_prop_value
            prop_num += prop_value / mitama_growth[prop][u"最小成长值"]

        if prop_num >= es_prop_num:
            return True
        else:
            return False

    return filter(es_prop_num_le_min, data_list)


def filter_mitama_type(data_list, mitama_type_list):
    def mitama_type_in_list(mitama):
        mitama_info = mitama.values()[0]
        if mitama_info.get(u'御魂类型', '') in mitama_type_list:
            return True
        else:
            return False

    return filter(mitama_type_in_list, data_list)


def filter_mitama(mitama_comb_list, mitama_type_limit,
                  prop_limit, upper_prop_limit, total_comb,
                  all_suit=True):

    mitama_sum_data = fit_mitama_type(mitama_comb_list, mitama_type_limit,
                                      total_comb, all_suit)

    for prop_type, prop_min_value in prop_limit.items():
        if prop_type in upper_prop_limit:
            prop_max_value = upper_prop_limit.pop(prop_type)
        else:
            prop_max_value = sys.maxsize
        mitama_sum_data = fit_prop_value(mitama_sum_data, prop_type,
                                         prop_min_value, prop_max_value)

    for prop_type, prop_max_value in upper_prop_limit.items():
        mitama_sum_data = fit_prop_value(mitama_sum_data, prop_type,
                                         0, prop_max_value)

    comb_data_list = cal_mitama_comb_prop(mitama_sum_data)

    return comb_data_list


def fit_mitama_type(mitama_comb_list, mitama_type_limit, total_comb,
                    all_suit):
    calculated_count = 0
    printed_rate = 0
    sys.stdout.flush()

    for mitama_comb in mitama_comb_list:
        calculated_count += 1

        mitama_type_count = {}
        mitama_enhance_count = {}
        for mitama in mitama_comb:
            mitama_info = mitama.values()[0]

            mitama_type = mitama_info.get(u'御魂类型')
            if mitama_type not in mitama_type_count:
                mitama_type_count[mitama_type] = 1
            else:
                mitama_type_count[mitama_type] += 1

        if all_suit:
            is_suit = True
            for _, count in mitama_type_count.items():
                if count < 2:
                    is_suit = False
            if not is_suit:
                continue

        comb_data = {'sum': {u'御魂计数': mitama_type_count},
                     'info': mitama_comb}

        printed_rate = print_cal_rate(calculated_count,
                                      total_comb, printed_rate)

        yield comb_data


def fit_prop_value(mitama_sum_data, prop_type, min_value, max_value):
    mitama_enhance = data_format.MITAMA_ENHANCE

    for mitama_data in mitama_sum_data:
        mitama_type_count = mitama_data['sum'].get(u'御魂计数')
        mitama_comb = mitama_data['info']
        prop_value = 0

        for mitama in mitama_comb:
            mitama_info = mitama.values()[0]
            if mitama_info.get(prop_type, 0):
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

        if min_value <= prop_value <= max_value:
            yield mitama_data


def cal_total_damage(mitama_comb, base_att, base_critdamage):
    """Calculate total damage

    Args:
        mitama_comb (dict): Mitama combination
        base_att (float): base attack
        base_hitdamage (float): base critical damage

    Returns:
        float: total_damage
    """
    sum_data = mitama_comb['sum']
    m_att = float(sum_data[u'攻击'] if sum_data[u'攻击'] else 0)
    m_att_en = float(sum_data[u'攻击加成'] if sum_data[u'攻击加成'] else 0)
    m_critdamage = float(sum_data[u'暴击伤害'] if sum_data[u'暴击伤害'] else 0)
    total_damage = ((base_att * (1 + m_att_en / 100) + m_att) *
                    (base_critdamage + m_critdamage) / 100)
    return total_damage


def cal_hp_crit(mitama_comb, base_hp, base_critdamage):
    sum_data = mitama_comb['sum']
    m_hp = float(sum_data[u'生命'] if sum_data[u'生命'] else 0)
    m_hp_en = float(sum_data[u'生命加成'] if sum_data[u'生命加成'] else 0)
    m_critdamage = float(sum_data[u'暴击伤害'] if sum_data[u'暴击伤害'] else 0)
    total_hp_crit = ((base_hp * (1 + m_hp_en / 100) + m_hp) *
                     (base_critdamage + m_critdamage) / 100)
    return total_hp_crit


def fit_damage_limit(mitama_comb_list, base_att, base_critdamage,
                     damage_limit):
    return fit_mitama_lambda(mitama_comb_list,
                             lambda x: cal_total_damage(x, base_att,
                                                        base_critdamage) >=
                             damage_limit)


def fit_hp_crit_limit(mitama_comb_list, base_hp, base_critdamage,
                      hp_crit_limit):
    return fit_mitama_lambda(mitama_comb_list,
                             lambda x: cal_hp_crit(x, base_hp,
                                                   base_critdamage) >=
                             hp_crit_limit)


def fit_mitama_lambda(mitama_comb_list, filter_func):
    """Filter the mitama combination by a customized function

    Args:
        mitama_comb_list (function): mitama combination list
        filter_func (function): customized function

    Returns:
        TYPE: return the filterd mitama combination list
    """
    for mitama_comb in mitama_comb_list:
        if filter_func(mitama_comb):
            yield mitama_comb


def cal_mitama_comb_prop(mitama_sum_data):
    for mitama_data in mitama_sum_data:
        mitama_type_count = mitama_data['sum'].get(u'御魂计数')
        mitama_comb = mitama_data['info']

        comb_sum = sum_prop(mitama_comb, mitama_type_count)

        comb_data = {'sum': comb_sum,
                     'info': mitama_comb}
        yield comb_data


def sum_prop(mitama_comb, mitama_type_count):
    prop_type_list = data_format.MITAMA_COL_NAME_ZH[3::]
    sum_result = {k: 0 for k in prop_type_list}
    mitama_enhance = data_format.MITAMA_ENHANCE

    for mitama in mitama_comb:
        mitama_info = mitama.values()[0]

        # 计算除套装外的总属性
        for prop_type in prop_type_list:
            if mitama_info.get(prop_type, 0):
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


def print_cal_rate(calculated_count, total_comb, printed_rate, rate=5):
    '''print cal rate in real time'''
    cal_rate = int(calculated_count * 100.0 / total_comb)
    if cal_rate > printed_rate and cal_rate % rate == 0:
        print('Calculating rate %s%%' % cal_rate)
        sys.stdout.flush()
        return cal_rate

    return printed_rate
