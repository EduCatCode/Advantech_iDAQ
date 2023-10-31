#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

if sys.platform.startswith('win32'):
    import msvcrt
elif sys.platform.startswith('linux'):
    import atexit
    from select import select

def kbhit():
    ''' Returns True if keyboard character was hit, False otherwise.
    '''
    if sys.platform.startswith('win32'):
        return msvcrt.kbhit()   
    else:
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []