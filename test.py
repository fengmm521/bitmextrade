#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

# from magetool import urltool

import sys
import os
import time



def getData():
    a = 1.0
    b = 2.0
    return a,b

def main():
    x = getData()
    print(x,type(x[0]),type(x[1]))

    if x[0] > 1.5:
        print('aaa')
    elif x[0] < 1.5:
        print('bbb')

def testtime():
    # 2018-03-03T08:14:49.225Z
    a = "2018-03-03T08:14:49.225Z"
    print time.mktime(time.strptime(a,"%Y-%m-%dT%H:%M:%S.%fZ"))

if __name__ == '__main__':
    testtime()

