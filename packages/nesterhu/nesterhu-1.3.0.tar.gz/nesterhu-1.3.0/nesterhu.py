# -*- coding: utf-8 -*-
"""
This is the  "neater.py" module and it provides one function called print_lol()
which prints lists that may or may not include neseted lists.

"""
import sys
def print_lol(the_list, indent = False, level = 0, fh = sys.stdout):
    
    """
    This function takes one postional argument called "the list", which
    is any python list(of - possibly - nested lists). Each data item in the
    provided list is(recuraively) printed to the screen on in's own line.
    The second parameter is used to insert tabs when a nested list is
    encountered.
    
    """
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fh)
        else:
            if indent:
                print("\t" * level, end = '', file = fh)
            print(each_item, file = fh)
            
