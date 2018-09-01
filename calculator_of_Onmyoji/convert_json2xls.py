#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

import load_data
import write_data


def get_json_files():
    work_path = os.getcwd()
    json_files = []

    for f in os.listdir(work_path):
        file_path = os.path.join(work_path, f)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_path)

            if file_extension == 'json':
                json_files.append(file_path)

    return json_files


if __name__ == '__main__':
    json_files = get_json_files()
    if not json_files:
        print('There is no json file in current directory, exit.')
        sys.exit(1)

    for file_path in json_files:
        data = load_data.get_mitama_data_json(file_path, [])

        file_name, _ = os.path.splitext(file_path)
        file_name_xls = file_name + '.xls'

        write_data.write_original_mitama_data(file_name_xls, data)

        print('File %s has been converted' % file_path)
