#!/usr/bin/python2
# coding: utf-8

import argparse

from calculator_of_Onmyoji import cal_and_filter as cal
from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


parser = argparse.ArgumentParser()
parser.add_argument("source_data",
                    type=str,
                    help=u'御魂数据表格，格式参照example/data_Template.xlsx')
parser.add_argument("output_file",
                    type=str,
                    help=u'输出文件位置，格式为pathto/filename.xls')
parser.add_argument("-M", "--mitama-suit",
                    type=str,
                    default=',0',
                    help=u'期望的御魂x件套类型，'
                         u'例如"-M 针女,4"为针女至少4件')
parser.add_argument("-P", "--prop-limit",
                    type=str,
                    default=',0',
                    help=u'期望限制的属性类型，'
                         u'例如"-P 暴击,90"为暴击至少90')
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


def main():
    args = parser.parse_args()
    file_name = args.source_data
    # solve problem with get utf8 args from shell
    mitama_suit = args.mitama_suit.decode('utf8')
    mitama_type, type_min_num = mitama_suit.split(',')

    prop_limit = args.prop_limit.decode('utf8')
    prop_type, prop_min_value = prop_limit.split(',')

    origin_data = load_data.get_mitama_data(file_name)
    suit_enhance = load_data.get_mitama_enhance(file_name)
    print('load data finish')

    locate_sep_data = load_data.sep_mitama_by_loc(origin_data)
    print('sep data by loc finish')
    mitama_comb = cal.make_combination(locate_sep_data)
    print('make combination finish')

    filter_result = cal.filter_mitama(mitama_comb, suit_enhance,
                                      mitama_type=mitama_type,
                                      type_min_num=int(type_min_num),
                                      prop_type=prop_type,
                                      prop_min_value=int(prop_min_value))
    print('filter mitama finish')

    write_data.write_mitama_result(args.output_file, filter_result)


if __name__ == '__main__':
    # test
    main()
