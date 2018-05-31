# coding: utf-8

import itertools


def make_combination(data_dict):
    if len(data_dict) != 6:
        raise KeyError("combination dict source must have 6 keys")

    d1, d2, d3, d4, d5, d6 = data_dict.values()
    return list(itertools.product(d1, d2, d3, d4, d5, d6))


if __name__ == '__main__':
    # test
    import load_data
    test_file = './example/data_Template.xlsx'
    d = load_data.get_mitama_data(test_file)
    l_d = load_data.sep_mitama_by_loc(d)

    com = make_combination(l_d)
    for i in com:
        print(i)

