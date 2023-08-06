#!/usr/bin/python3
import sys
"""this program is for defining the range list"""
def print_range(the_list, indent=False, level=0):
    for  p_range in the_list:
        if isinstance(p_range, list):
            print_range(p_range, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(p_range)
