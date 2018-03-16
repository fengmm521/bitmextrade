#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

import os,commands



def main():
    # a = os.system('/Users/mage/Documents/tool/cmdtool/pspy')
    a,b = commands.getstatusoutput('/Users/mage/Documents/tool/cmdtool/pspy')
    print(a)
    print(b)

if __name__ == "__main__":
    main()


   
