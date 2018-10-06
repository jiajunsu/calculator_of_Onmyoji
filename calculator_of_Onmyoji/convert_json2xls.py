#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

from calculator_of_Onmyoji import load_data
from calculator_of_Onmyoji import write_data


if __name__ == '__main__':
    json_files = load_data.get_ext_files('.json')
    if not json_files:
        print('There is no json file in current directory, exit.')
        sys.exit(1)

    for file_path in json_files:
        data = load_data.get_mitama_data_json(file_path, [])

        file_name, _ = os.path.splitext(file_path)
        file_name_xls = file_name + '.xls'

        write_data.write_original_mitama_data(file_name_xls, data)

        print('File %s has been converted' % file_path)
