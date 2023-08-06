#!/usr/bin/env python
# encoding: utf-8
'''
@author: baige
@license: (C) Copyright 2018
@contact: jeckerWen@gmail.com
@file: nester_wrj.py
@Date: 2019/2/28 18:50
@desc:
'''



def print_lol(the_list, indent=False, level=0):
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent=indent, level=level + 1)
        else:
            if indent:
                for tab in range(level):
                    print('--', end='')
            print(item)

