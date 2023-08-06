#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:05:20 2019
 test pypi 
@author: liuxiaoyan
"""

def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,type(list)):
            print_lol(each_item,indent,level+1)
        else:
            if  indent:
                for tab_stop in range(level):
                    print('\t',end='')            
            print(each_item)
            
 
