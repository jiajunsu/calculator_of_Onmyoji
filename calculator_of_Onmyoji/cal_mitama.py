#!/usr/bin/python2
# coding: utf-8

import argparse
import locale
import platform

from calculator_of_Onmyoji import cal_and_filter as cal
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


sysstr = platform.system()
encoding = locale.getpreferredencoding()

parser = argparse.ArgumentParser()
parser.add_argument("source_data",
                    type=str,
                    help=u'御魂数据表格，格式参照example/data_Template.xls')
parser.add_argument("output_file",
                    type=str,
                    help=u'输出文件位置，格式为pathto/filename.xls')
parser.add_argument("-M", "--mitama-suit",
                    type=str,
                    default=',0',
                    help=u'期望的御魂x件套类型，多个限制用英文句号.间隔，'
                         u'例如"-M 针女,4"为针女至少4件，'
                         u'"-M 针女,4.破势,2"为针女4件+破势2件')
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
                         u'例如"-2P 攻击加成,55"为二号位攻击加成至少55')
parser.add_argument("-4P", "--fth-prop-value",
                    type=str,
                    default=',0',
                    help=u'四号位限制的属性类型和数值，'
                         u'例如"-4P 攻击加成,55"为四号位攻击加成至少55')
parser.add_argument("-6P", "--sth-prop-value",
                    type=str,
                    default=',0',
                    help=u'六号位限制的属性类型和数值，'
                         u'例如"-6P 暴击,55"为六号位暴击至少55')
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


def sep_utf_str(utf_str):
    # solve problem with get utf8 args from shell
    if sysstr == 'Windows':
        try:
            uni_str = utf_str.decode(encoding)
        except UnicodeDecodeError:
            print('Error in decode %s' % utf_str)
            raise
    else:
        uni_str = utf_str.decode('utf8')
    if ',' in uni_str:
        return uni_str.split(',')
    else:
        return [uni_str]


def sep_utf_str_to_dict(utf_str):
    if not utf_str:
        return dict()

    if sysstr == 'Windows':
        try:
            uni_str = utf_str.decode(encoding)
        except UnicodeDecodeError:
            print('Error in decode %s' % utf_str)
            raise
    else:
        uni_str = utf_str.decode('utf8')
    limit_list = uni_str.split('.')
    formated_dict = dict()
    for limit in limit_list:
        if ',' not in limit:
            continue
        key, value = limit.split(',')
        formated_dict[key] = int(value)
    return formated_dict


def main():
    args = parser.parse_args()
    print('Input args: %s' % args)
    print('System encoding=%s' % encoding)

    file_name = args.source_data

    mitama_type_limit = sep_utf_str_to_dict(args.mitama_suit)
    prop_limit = sep_utf_str_to_dict(args.prop_limit)
    upper_prop_limit = sep_utf_str_to_dict(args.upper_prop_limit)

    l2_prop, l2_prop_value = sep_utf_str(args.sec_prop_value)
    l4_prop, l4_prop_value = sep_utf_str(args.fth_prop_value)
    l6_prop, l6_prop_value = sep_utf_str(args.sth_prop_value)

    ignore_serial = sep_utf_str(args.ignore_serial)

    base_att, base_critdamage_att, damage_limit = \
        map(float, sep_utf_str(args.damage_limit))

    base_hp, base_critdamage_hp, hp_crit_limit = \
        map(float, sep_utf_str(args.health_limit))

    if (base_critdamage_att and base_critdamage_hp and
            base_critdamage_att != base_critdamage_hp):
        print('WARN: crit_damage between DL and HL is different')

    if base_critdamage_att:
        base_critdamage = base_critdamage_att
    else:
        base_critdamage = base_critdamage_hp

    origin_data = load_data.get_mitama_data(file_name, ignore_serial)
    print('Loading data finish')

    locate_sep_data = load_data.sep_mitama_by_loc(origin_data)

    print('Start calculating')
    locate_sep_data = cal.filter_loc(locate_sep_data,
                                     l2_prop, int(l2_prop_value),
                                     l4_prop, int(l4_prop_value),
                                     l6_prop, int(l6_prop_value))

    mitama_comb = cal.make_combination(locate_sep_data,
                                       mitama_type_limit, args.all_suit)

    filter_result = cal.filter_mitama(mitama_comb,
                                      mitama_type_limit,
                                      prop_limit,
                                      upper_prop_limit,
                                      all_suit=args.all_suit)

    if damage_limit > 0:
        filter_result = cal.fit_damage_limit(filter_result, base_att,
                                             base_critdamage, damage_limit)
    if hp_crit_limit > 0:
        filter_result = cal.fit_hp_crit_limit(filter_result, base_hp,
                                              base_critdamage, hp_crit_limit)

    write_data.write_mitama_result(args.output_file, filter_result,
                                   base_att, base_hp, base_critdamage)


if __name__ == '__main__':
    main()
