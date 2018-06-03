#!/usr/bin/python2
# coding: utf-8

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("source_data",
                    type=str,
                    help=u'御魂数据表格，格式参照example/data_Template.xlsx')
parser.add_argument("-M", "--mitama-suit",
                    type=unicode,
                    help=u'期望的御魂x件套类型，例如"-M 针女 -N 4"为针女至少4件')
parser.add_argument("-N", "--mitama-min-num",
                    type=int,
                    choices=range(1, 7),
                    help=u'期望的御魂x件套的最小件数，例如"-M 针女 -N 4"为针女至少4件')
parser.add_argument("-P", "--prop-type",
                    type=unicode,
                    help=u'期望限制的属性类型，例如"-P 暴击 -V 90"为暴击至少90')
parser.add_argument("-V", "--prop-min-value",
                    type=int,
                    help=u'期望属性的最小值，例如"-P 暴击 -V 90"为暴击至少90')


def main():
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    # test
    main()
