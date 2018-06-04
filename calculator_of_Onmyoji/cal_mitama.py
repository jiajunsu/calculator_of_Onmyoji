#!/usr/bin/python2
# coding: utf-8

import argparse

from calculator_of_Onmyoji import cal_and_filter
from calculator_of_Onmyoji import load_data


parser = argparse.ArgumentParser()
parser.add_argument("source_data",
                    type=str,
                    help=u'御魂数据表格，格式参照example/data_Template.xlsx')
parser.add_argument("-M", "--mitama-suit",
                    type=str,
                    default='',
                    help=u'期望的御魂x件套类型，例如"-M 针女 -N 4"为针女至少4件')
parser.add_argument("-N", "--mitama-min-num",
                    type=int,
                    default=0,
                    choices=range(1, 7),
                    help=u'期望的御魂x件套的最小件数，例如"-M 针女 -N 4"为针女至少4件')
parser.add_argument("-P", "--prop-type",
                    type=str,
                    default='',
                    help=u'期望限制的属性类型，例如"-P 暴击 -V 90"为暴击至少90')
parser.add_argument("-V", "--prop-min-value",
                    type=int,
                    default=0,
                    help=u'期望属性的最小值，例如"-P 暴击 -V 90"为暴击至少90')


def main():
    args = parser.parse_args()
    file_name = args.source_data
    
    origin_data = load_data.get_mitama_data(file_name)
    suit_enhance = load_data.get_mitama_enhance(file_name)

    locate_sep_data = load_data.sep_mitama_by_loc(origin_data)
    mitama_comb = cal_and_filter.make_combination(locate_sep_data)

    filter_result = cal_and_filter.filter_mitama(mitama_comb, suit_enhance,
                                                 mitama_type=args.mitama_suit.decode('utf8'),
                                                 type_min_num=args.mitama_min_num,
                                                 prop_type=args.prop_type.decode('utf8'),
                                                 prop_min_value=args.prop_min_value) 
    
    print(len(filter_result))


if __name__ == '__main__':
    # test
    main()
