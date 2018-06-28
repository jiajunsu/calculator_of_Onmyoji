#!/usr/bin/python2
# coding: utf-8
import os
from cal_mitama import total_damage
from collections import defaultdict
from heapq import heappush, heappop
import write_data



def mitama_comb_nonoverlap(comb_data_list, path_to_output, MAX_OUTPUT = 5):
    """Analyze the mitama combinations, and output non-overlapping mitama combos 
    in the same file

    Args:
        comb_data_list (list): list of mitama combinations
        path_to_output (str): output file path
    """
    base_att, base_critdamage = 3216, 150
    serial_num = 0
    m2c = defaultdict(set)
    c2m = defaultdict(set)
    sorted_comb_list = []
    
    for comb_data in comb_data_list:
        # first row of each comb_data is sum info
        sum_data = comb_data.get('sum', {})
        tdmg = total_damage(comb_data, base_att, base_critdamage)
        sorted_comb_list.append((base_att/tdmg, serial_num, tdmg, comb_data))
        
        # write each mitama data into detail file
        mitama_data = comb_data.get('info', set())
        for mitama in mitama_data:
            mitama_serial = mitama.keys()[0]
            #mitama_prop = mitama[mitama_serial]
            c2m[serial_num].add(mitama_serial)
            m2c[mitama_serial].add(serial_num)

        serial_num += 1
    
    def mark_conflict(com_serial):
        for mitama_serial in c2m[com_serial]:
            for conflict_comb in m2c[mitama_serial]:
                if conflict_comb in valid:
                    valid.remove(conflict_comb)

    num_com = serial_num
    filename, file_extension = os.path.splitext(path_to_output)


    for start_idx in range(MAX_OUTPUT):
        valid = set(range(num_com))
        choices = []
        for i in range(start_idx, num_com):
            _, com_serial, tdmg, comb_data = sorted_comb_list[i]
            if com_serial in valid:
                choices.append(comb_data)
                mark_conflict(com_serial)
            if not valid:
                break
        new_fname = "{}-{}{}".format(filename, start_idx, file_extension)
        write_data.write_mitama_result(new_fname, choices)


