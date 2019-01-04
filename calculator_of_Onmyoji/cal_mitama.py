#!/usr/bin/python2
# coding: utf-8

import argparse
import locale

from calculator_of_Onmyoji import cal_and_filter as cal
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


code_t = locale.getpreferredencoding()


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def locale_decode(utf_str):
    try:
        uni_str = utf_str.decode(code_t)
        return uni_str
    except UnicodeDecodeError:
        print('Decode failed %s' % utf_str)
        raise UnicodeDecodeError


def sep_utf_str(utf_str):
    uni_str = locale_decode(utf_str)
    if ',' in uni_str:
        return uni_str.split(',')
    else:
        return [uni_str]


def sep_utf_str_to_list(utf_str):
    if not utf_str:
        return dict()

    uni_str = locale_decode(utf_str)
    limit_list = uni_str.split('.')
    formated_list = list()
    for limit in limit_list:
        if ',' not in limit:
            continue
        key, value = limit.split(',')
        if key:
            formated_list.append((key, int(value)))
    return formated_list


def sep_utf_str_to_dict(utf_str):
    if not utf_str:
        return dict()

    uni_str = locale_decode(utf_str)
    limit_list = uni_str.split('.')
    formated_dict = dict()
    for limit in limit_list:
        if ',' not in limit:
            continue
        key, value = limit.split(',')
        if key:
            formated_dict[key] = int(value)
    return formated_dict


class Calculator(object):
    def __init__(self, params=None):
        if not params:
            self._init_from_args()
        else:
            self.init_from_params(params)

    def _init_from_args(self):
        args = self._get_args()
        print('Input args: %s' % args)

        self.file_name = args.source_data
        self.output_file = args.output_file

        self.mitama_type_limit = sep_utf_str_to_list(args.mitama_suit)
        self.prop_limit = sep_utf_str_to_dict(args.prop_limit)
        self.upper_prop_limit = sep_utf_str_to_dict(args.upper_prop_limit)

        self.l2_prop_limit = sep_utf_str_to_dict(args.sec_prop_value)
        self.l4_prop_limit = sep_utf_str_to_dict(args.fth_prop_value)
        self.l6_prop_limit = sep_utf_str_to_dict(args.sth_prop_value)

        self.all_suit = args.all_suit
        self.attack_only = args.attack_only

        if args.effective_secondary_prop:
            self.es_prop = sep_utf_str(args.effective_secondary_prop)
            self.es_prop_num = \
                map(int, sep_utf_str(args.effective_secondary_prop_num))
        else:
            self.es_prop = None
            self.es_prop_num = None

        self.ignore_serial = sep_utf_str(args.ignore_serial)

        self.base_att, self.base_critdamage_att, self.damage_limit = \
            map(float, sep_utf_str(args.damage_limit))

        self.base_hp, self.base_critdamage_hp, self.hp_crit_limit = \
            map(float, sep_utf_str(args.health_limit))

        if (self.base_critdamage_att and self.base_critdamage_hp and
                self.base_critdamage_att != self.base_critdamage_hp):
            print('WARN: crit_damage between DL and HL is different')

        if self.base_critdamage_att:
            self.base_critdamage = self.base_critdamage_att
        else:
            self.base_critdamage = self.base_critdamage_hp

    def _get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("source_data",
                            type=str,
                            help=u'御魂数据，格式参照example/data_Template.xls')
        parser.add_argument("output_file",
                            type=str,
                            help=u'输出文件位置，格式为pathto/filename.xls')
        parser.add_argument("-M", "--mitama-suit",
                            type=str,
                            default=',0',
                            help=u'期望的x件套御魂类型或者加成类型，'
                                 u'多个限制用英文句号.间隔，'
                                 u'例如"-M 针女,4"为针女至少4件，'
                                 u'"-M 针女,4.破势,2"为针女4件+破势2件，'
                                 u'"-M 生命加成,2.生命加成,2.生命加成,2"为3个生命两件套')
        parser.add_argument("-P", "--prop-limit",
                            type=str,
                            default='',
                            help=u'期望限制的属性下限，多个属性条件用英文句号.间隔, '
                                 u'例如"-P 暴击,90.暴击伤害,70"为暴击至少90'
                                 u'且暴击伤害至少70')
        parser.add_argument("-UP", "--upper-prop-limit",
                            type=str,
                            default='',
                            help=u'期望限制的属性上限，多个属性条件用英文句号.间隔，'
                                 u'例如"-UP 暴击,95.速度,20"为暴击最多95'
                                 u'且速度最多20')
        parser.add_argument("-2P", "--sec-prop-value",
                            type=str,
                            default=',0',
                            help=u'二号位限制的属性类型和数值，'
                                 u'多个属性用英文句号.间隔，'
                                 u'例如"-2P 攻击加成,55"为二号位攻击加成至少55')
        parser.add_argument("-4P", "--fth-prop-value",
                            type=str,
                            default=',0',
                            help=u'四号位限制的属性类型和数值，'
                                 u'多个属性用英文句号.间隔，'
                                 u'例如"-4P 攻击加成,55"为四号位攻击加成至少55')
        parser.add_argument("-6P", "--sth-prop-value",
                            type=str,
                            default=',0',
                            help=u'六号位限制的属性类型和数值，'
                                 u'多个属性用英文句号.间隔，'
                                 u'例如"-6P 暴击,55"为六号位暴击至少55，'
                                 u'"-6P 暴击,55.暴击伤害,89"为六号位暴击至少55'
                                 u'或暴击伤害至少89')
        parser.add_argument("-IG", "--ignore-serial",
                            type=str,
                            default='',
                            help=u'忽略的御魂序号关键字，用逗号,间隔'
                                 u'例如"-IG 天狗,鸟"为御魂序号包含天狗或鸟则滤除')
        parser.add_argument("-AS", "--all-suit",
                            type=str2bool,
                            default=True,
                            help=u'是否全为套装，默认为True。'
                                 u'"-AS False"为允许非套装的组合出现，如5针女1破势')
        parser.add_argument("-DL", "--damage-limit",
                            type=str,
                            default='0,0,0',
                            help=u'基础攻击,基础暴伤,期望的攻击*暴伤，'
                                 u'例如"-DL 3126,150，20500"，当基础攻击为3126，'
                                 u'基础暴伤为150，攻击*暴伤>=20500')
        parser.add_argument("-HL", "--health-limit",
                            type=str,
                            default='0,0,0',
                            help=u'基础生命,基础暴伤,期望的生命*暴伤，'
                                 u'例如"-HL 8000,150,60000"，当基础生命为8000，'
                                 u'基础暴伤为150，生命*暴伤>=60000')
        parser.add_argument("-AO", "--attack-only",
                            type=str2bool,
                            default=False,
                            help=u'是否只计算输出类御魂，默认为False。'
                                 u'"-AO True"为只计算套装属性为攻击加成、'
                                 u'暴击和首领御魂的套装组合')
        parser.add_argument("-ESP", "--effective-secondary-prop",
                            type=str,
                            default='',
                            help=u'设定御魂的有效副属性，用逗号,间隔'
                                 u'例如"-ESP 暴击,暴击伤害,速度,攻击加成"'
                                 u'意味着有效副属性定位为暴击、暴击伤害、速度、攻击加成')
        parser.add_argument("-ESPN", "--effective-secondary-prop-num",
                            type=str,
                            default='',
                            help=u'限定1-6号位御魂的有效副属性加成次数，用逗号,间隔'
                                 u'与-ESP配合使用'
                                 u'例如"-ESP 暴击 -ESPN 5,3,5,3,5,0"'
                                 u'意味着1~6号位各自的有效副属性加成次数'
                                 u'依次不少于5,3,5,3,5,0'
                                 u'1号位副属性暴击加成次数不少于5'
                                 u'即暴击不低于12(2.4*5)')
        return parser.parse_args()

    def init_from_params(self, param_dict):
        print('Input params %s' % str(param_dict))
        for key, value in param_dict.iteritems():
            setattr(self, key, value)

    def run(self):
        origin_data = load_data.get_mitama_data(self.file_name,
                                                self.ignore_serial)
        print('Loading data finish')

        locate_sep_data = load_data.sep_mitama_by_loc(origin_data)

        print('Start calculating')
        locate_sep_data = cal.filter_loc_and_type(locate_sep_data,
                                                  self.l2_prop_limit,
                                                  self.l4_prop_limit,
                                                  self.l6_prop_limit,
                                                  self.mitama_type_limit,
                                                  self.attack_only,
                                                  self.es_prop,
                                                  self.es_prop_num)

        mitama_comb, total_comb = cal.make_combination(locate_sep_data,
                                                       self.mitama_type_limit,
                                                       self.all_suit)

        filter_result = cal.filter_mitama(mitama_comb,
                                          self.mitama_type_limit,
                                          self.prop_limit,
                                          self.upper_prop_limit,
                                          total_comb,
                                          all_suit=self.all_suit)

        if self.damage_limit > 0:
            filter_result = cal.fit_damage_limit(filter_result,
                                                 self.base_att,
                                                 self.base_critdamage,
                                                 self.damage_limit)
        if self.hp_crit_limit > 0:
            filter_result = cal.fit_hp_crit_limit(filter_result,
                                                  self.base_hp,
                                                  self.base_critdamage,
                                                  self.hp_crit_limit)

        write_data.write_mitama_result(self.output_file,
                                       filter_result,
                                       self.es_prop,
                                       self.base_att,
                                       self.base_hp,
                                       self.base_critdamage)


if __name__ == '__main__':
    calculator = Calculator()
    calculator.run()
