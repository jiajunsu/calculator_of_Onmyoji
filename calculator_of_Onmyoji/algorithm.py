# coding: utf-8

import itertools
import sys

from calculator_of_Onmyoji import data_format
from functools import reduce


class MitamaComb(object):
    def __init__(self, locate_sep_data,
                 l2_prop_limit, l4_prop_limit, l6_prop_limit,
                 mitama_type_limit, all_suit, attack_only,
                 es_prop, es_prop_num,
                 prop_limit, upper_prop_limit,
                 base_att, base_critdamage, damage_limit, attack_buff,
                 base_hp, hp_crit_limit):

        self.locate_sep_data = locate_sep_data
        self.l2_prop_limit = l2_prop_limit
        self.l4_prop_limit = l4_prop_limit
        self.l6_prop_limit = l6_prop_limit
        self.mitama_type_limit = mitama_type_limit
        self.all_suit = all_suit
        self.attack_only = attack_only
        self.es_prop = es_prop
        self.es_prop_num = es_prop_num
        self.prop_limit = prop_limit
        self.upper_prop_limit = upper_prop_limit
        self.base_att = base_att
        self.base_critdamage = base_critdamage
        self.damage_limit = damage_limit
        self.attack_buff = attack_buff
        self.base_hp = base_hp
        self.hp_crit_limit = hp_crit_limit

        self.total_comb = 0
        self.calculated_count = 0

    def filter_loc_and_type(self):
        print('mitama nums by loc is %s'
              % str([len(d) for d in list(self.locate_sep_data.values())]))

        if self.attack_only:
            # 只计算输出类御魂,已选定的御魂套装不过滤
            selected_types = [t for t, _ in self.mitama_type_limit]
            filter_types = selected_types + data_format.ATTACK_MITAMA_TYPE
            for loc, data in self.locate_sep_data.items():
                self.locate_sep_data[loc] = \
                    self.filter_mitama_type(data, filter_types)

        # 246号位主属性过滤
        if self.l2_prop_limit:
            self.locate_sep_data[2] = \
                self.filter_loc_prop(self.locate_sep_data[2],
                                     self.l2_prop_limit)
        if self.l4_prop_limit:
            self.locate_sep_data[4] = \
                self.filter_loc_prop(self.locate_sep_data[4],
                                     self.l4_prop_limit)
        if self.l6_prop_limit:
            self.locate_sep_data[6] = \
                self.filter_loc_prop(self.locate_sep_data[6],
                                     self.l6_prop_limit)

        # 全位置副属性过滤
        if self.es_prop and self.es_prop_num:
            for loc, data_list in self.locate_sep_data.items():
                self.locate_sep_data[loc] = \
                    self.filter_effective_secondary_prop(
                        data_list, self.es_prop_num[loc-1])

        print('after filter by loc prop and type %s'
              % str([len(d) for d in list(self.locate_sep_data.values())]))

        self.locate_sep_data = dict(zip(range(1, 7),
                                        [d for d in
                                         self.locate_sep_data.values()]))

    def find_mtype_candidates(self, mitama_type='ALL'):
        candidates = []
        if mitama_type == 'ALL':
            candidates = data_format.MITAMA_TYPES
        elif mitama_type in data_format.MITAMA_TYPES:
            candidates.append(mitama_type)
        elif mitama_type in data_format.MITAMA_PROPS:
            for m_type in data_format.MITAMA_TYPES:
                if (data_format.MITAMA_ENHANCE[m_type]["加成类型"] ==
                        mitama_type or
                        not data_format.MITAMA_ENHANCE[m_type]["加成类型"]):
                    candidates.append(m_type)
        return candidates

    def gen_mitama_combos(self):
        main_type, secondary_type = None, []
        fixed_pos = 0
        for m_type, limit_count in self.mitama_type_limit:
            if m_type not in (data_format.MITAMA_TYPES +
                              data_format.MITAMA_PROPS):
                continue
            if limit_count == 4:
                main_type = m_type
                fixed_pos += 4
            elif limit_count == 2:
                secondary_type.append(m_type)
                fixed_pos += 2

        if main_type is not None:
            main_candidates = self.find_mtype_candidates(main_type)
            if fixed_pos == 6 or self.all_suit:  # 4+2
                if secondary_type:
                    secondary_candidates = \
                        self.find_mtype_candidates(secondary_type[0])
                elif self.all_suit:
                    secondary_candidates = self.find_mtype_candidates()
                for m_type in main_candidates:
                    for s_type in secondary_candidates:
                        yield [m_type] * 4 + [s_type] * 2
            else:       # 4+1+1
                yield [m_type] * 4 + ['ALL', 'ALL']

        elif fixed_pos == 6 or (self.all_suit and fixed_pos >= 2):
            # 2+2+2, 2+2+any, 2+any+any
            candidates = []
            for m_type in secondary_type:
                candidates.append(self.find_mtype_candidates(m_type))
            for i in range((6-fixed_pos)//2):
                candidates.append(self.find_mtype_candidates())
            generated = {}
            for t1, t2, t3 in itertools.product(*candidates):
                if frozenset((t1, t2, t3)) not in generated and\
                   t1 != t2 and t2 != t3 and t1 != t3:
                    generated[frozenset((t1, t2, t3))] = True
                    yield [t1, t2, t3]*2
        elif fixed_pos >= 2:
            candidates = []
            for m_type in secondary_type:
                candidates.append(self.find_mtype_candidates(m_type))

            for i in range(6-fixed_pos):
                candidates.append(["ALL"])
            generated = {}
            for combo in itertools.product(*candidates):
                if len(set(combo[:fixed_pos//2])) != fixed_pos//2:
                    continue
                t1, t2, t3, t4, t5, t6 = (combo[:fixed_pos//2]*2 +
                                          combo[fixed_pos//2:])
                if frozenset((t1, t2, t3, t4, t5, t6)) not in generated:
                    generated[frozenset((t1, t2, t3, t4, t5, t6))] = True
                    yield [t1, t2, t3, t4, t5, t6]
        else:
            yield None

    def gen_mitama_permutations(self):
        generated = {}
        for m_combos in self.gen_mitama_combos():
            if m_combos is None:
                yield None
            else:
                for m_permu in itertools.permutations(m_combos):
                    if tuple(m_permu) not in generated:
                        generated[tuple(m_permu)] = True
                        yield m_permu

    def make_combination(self):
        def filter_mitama_by_type(mitama, desired_type):
            mitama_info = list(mitama.values())[0]
            if mitama_info['御魂类型'] == desired_type:
                return True
            else:
                return False

        def classify_by_type():
            mitama_data_by_type = {}
            for m_type in data_format.MITAMA_TYPES:
                mitama_data_by_type[m_type] = {}
                for i in range(1, 7):
                    mitama_data_by_type[m_type][i] =\
                        [x for x in self.locate_sep_data[i]
                         if filter_mitama_by_type(x, m_type)]
            return mitama_data_by_type

        mitama_data_by_type = None
        res = []
        for m_combos in self.gen_mitama_permutations():
            if m_combos is None:
                self.total_comb = reduce(lambda x, y: x*y,
                                         map(len,
                                             self.locate_sep_data.values()))
                print("Total combinations: {}".format(self.total_comb))
                return itertools.product(*self.locate_sep_data.values())
            else:
                if mitama_data_by_type is None:
                    mitama_data_by_type = classify_by_type()
                mitama_grp = {x: self.locate_sep_data[x]
                              if m_type == 'ALL' else
                              mitama_data_by_type[m_type][x]
                              for x, m_type in zip(range(1, 7), m_combos)}
                self.total_comb += reduce(lambda x, y: x*y,
                                          map(len, mitama_grp.values()))
                res.append(itertools.product(*mitama_grp.values()))

        print("Total combinations: {}".format(self.total_comb))
        return itertools.chain(*res)

    def filter_loc_prop(self, data_list, prop_limit):
        def prop_value_le_min(mitama):
            mitama_info = list(mitama.values())[0]
            for prop_type, prop_min_value in prop_limit.items():
                if (mitama_info.get(prop_type, 0) and
                        mitama_info[prop_type] >= prop_min_value):
                    return True
            else:
                return False

        return list(filter(prop_value_le_min, data_list))

    def filter_effective_secondary_prop(self, data_list, es_prop_num):
        mitama_growth = data_format.MITAMA_GROWTH

        def es_prop_num_le_min(mitama):
            mitama_info = list(mitama.values())[0]
            prop_num = 0
            for prop in self.es_prop:
                prop_value = mitama_info.get(prop, 0.0)
                main_prop_value = mitama_growth[prop]["主属性"]
                if prop_value >= main_prop_value:
                    prop_value -= main_prop_value
                prop_num += prop_value / mitama_growth[prop]["最小成长值"]

            if prop_num >= es_prop_num:
                return True
            else:
                return False

        return list(filter(es_prop_num_le_min, data_list))

    def filter_mitama_type(self, data_list, mitama_type_list):
        def mitama_type_in_list(mitama):
            mitama_info = list(mitama.values())[0]
            if mitama_info.get('御魂类型', '') in mitama_type_list:
                return True
            else:
                return False

        return list(filter(mitama_type_in_list, data_list))

    def filter_mitama(self, mitama_comb_list):
        mitama_sum_data = self.fit_mitama_type(mitama_comb_list)

        for prop_type, prop_min_value in self.prop_limit.items():
            if prop_type in self.upper_prop_limit:
                prop_max_value = self.upper_prop_limit.pop(prop_type)
            else:
                prop_max_value = sys.maxsize
            mitama_sum_data = self.fit_prop_value(mitama_sum_data, prop_type,
                                                  prop_min_value,
                                                  prop_max_value)

        for prop_type, prop_max_value in self.upper_prop_limit.items():
            mitama_sum_data = self.fit_prop_value(mitama_sum_data, prop_type,
                                                  0, prop_max_value)

        comb_data_list = self.cal_mitama_comb_prop(mitama_sum_data)

        return comb_data_list

    def fit_mitama_type(self, mitama_comb_list):
        printed_rate = 0
        sys.stdout.flush()

        for mitama_comb in mitama_comb_list:
            self.calculated_count += 1

            mitama_type_count = {}
            for mitama in mitama_comb:
                mitama_info = list(mitama.values())[0]

                mitama_type = mitama_info.get('御魂类型')
                if mitama_type not in mitama_type_count:
                    mitama_type_count[mitama_type] = 1
                else:
                    mitama_type_count[mitama_type] += 1

            if self.all_suit:
                is_suit = True
                for _, count in mitama_type_count.items():
                    if count < 2:
                        is_suit = False
                if not is_suit:
                    continue

            comb_data = {'sum': {'御魂计数': mitama_type_count},
                         'info': mitama_comb}

            printed_rate = self.print_cal_rate(printed_rate)

            yield comb_data

    def fit_prop_value(self, mitama_sum_data, prop_type, min_value, max_value):
        mitama_enhance = data_format.MITAMA_ENHANCE

        for mitama_data in mitama_sum_data:
            mitama_type_count = mitama_data['sum'].get('御魂计数')
            mitama_comb = mitama_data['info']
            prop_value = 0

            for mitama in mitama_comb:
                mitama_info = list(mitama.values())[0]
                if mitama_info.get(prop_type, 0):
                    prop_value += mitama_info[prop_type]

            for m_type, m_count in mitama_type_count.items():
                if m_count < 2:
                    continue
                else:
                    p_type = mitama_enhance[m_type].get('加成类型')
                    if p_type == prop_type:
                        multi_times = 2 if m_count == 6 else 1  # 6个御魂算2次套装
                        prop_value += (
                            multi_times * mitama_enhance[m_type].get('加成数值'))

            if min_value <= prop_value <= max_value:
                yield mitama_data

    def cal_total_damage(self, mitama_comb):
        """Calculate total damage

        Args:
            mitama_comb (dict): Mitama combination
            base_att (float): base attack
            base_hitdamage (float): base critical damage

        Returns:
            float: total_damage
        """
        sum_data = mitama_comb['sum']
        m_att = float(sum_data['攻击'] if sum_data['攻击'] else 0)
        m_att_en = float(sum_data['攻击加成'] if sum_data['攻击加成'] else 0)
        m_critdamage = float(sum_data['暴击伤害'] if sum_data['暴击伤害'] else 0)
        total_damage = ((self.base_att * (1 + m_att_en / 100) + m_att
                         + self.base_att * self.attack_buff / 100) *
                        (self.base_critdamage + m_critdamage) / 100)
        return total_damage

    def cal_hp_crit(self, mitama_comb):
        sum_data = mitama_comb['sum']
        m_hp = float(sum_data['生命'] if sum_data['生命'] else 0)
        m_hp_en = float(sum_data['生命加成'] if sum_data['生命加成'] else 0)
        m_critdamage = float(sum_data['暴击伤害'] if sum_data['暴击伤害'] else 0)
        total_hp_crit = ((self.base_hp * (1 + m_hp_en / 100) + m_hp) *
                         (self.base_critdamage + m_critdamage) / 100)
        return total_hp_crit

    def fit_damage_limit(self, mitama_comb_list):
        return self.fit_mitama_lambda(mitama_comb_list,
                                      lambda x: self.cal_total_damage(x) >=
                                      self.damage_limit)

    def fit_hp_crit_limit(self, mitama_comb_list):
        return self.fit_mitama_lambda(mitama_comb_list,
                                      lambda x: self.cal_hp_crit(x) >=
                                      self.hp_crit_limit)

    def fit_mitama_lambda(self, mitama_comb_list, filter_func):
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

    def cal_mitama_comb_prop(self, mitama_sum_data):
        for mitama_data in mitama_sum_data:
            mitama_type_count = mitama_data['sum'].get('御魂计数')
            mitama_comb = mitama_data['info']

            comb_sum = self.sum_prop(mitama_comb, mitama_type_count)

            comb_data = {'sum': comb_sum,
                         'info': mitama_comb}
            yield comb_data

    def sum_prop(self, mitama_comb, mitama_type_count):
        prop_type_list = data_format.MITAMA_COL_NAME_ZH[3::]
        sum_result = {k: 0 for k in prop_type_list}
        mitama_enhance = data_format.MITAMA_ENHANCE

        for mitama in mitama_comb:
            mitama_info = list(mitama.values())[0]

            # 计算除套装外的总属性
            for prop_type in prop_type_list:
                if mitama_info.get(prop_type, 0):
                    sum_result[prop_type] += mitama_info[prop_type]

        for m_type, m_count in mitama_type_count.items():
            if m_count < 2:  # 忽略套装效果
                continue
            else:
                multi_times = 2 if m_count == 6 else 1  # 6个同类御魂算2次套装效果
                prop_type = mitama_enhance[m_type].get('加成类型')
                if prop_type:
                    sum_result[prop_type] += (
                        multi_times * mitama_enhance[m_type].get('加成数值'))

        return sum_result

    def print_cal_rate(self, printed_rate, rate=5):
        '''print cal rate in real time'''
        cal_rate = int(self.calculated_count * 100.0 / self.total_comb)
        if cal_rate > printed_rate and cal_rate % rate == 0:
            print('Calculating rate %s%%' % cal_rate)
            sys.stdout.flush()
            return cal_rate

        return printed_rate

    def get_comb(self):
        # 按御魂限制条件筛选剪枝
        self.filter_loc_and_type()
        # 生成全组合
        mitama_comb = self.make_combination()
        # 按组合属性上下限过滤
        filter_result = self.filter_mitama(mitama_comb)
        # 按攻击*暴伤过滤
        if self.damage_limit > 0:
            filter_result = self.fit_damage_limit(filter_result)
        # 按生命*暴伤过滤
        if self.hp_crit_limit > 0:
            filter_result = self.fit_hp_crit_limit(filter_result)

        return filter_result

    def get_progress(self):
        """Return calculating progress

        return value: percent, current, total
        """
        if self.total_comb <= 0:
            return 0, 0, 0
        return (float(self.calculated_count) / self.total_comb,
                self.calculated_count,
                self.total_comb)
