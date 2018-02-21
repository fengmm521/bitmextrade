#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-21 11:37:54
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys

src="https://static.bitmex.com/chartEmbed?symbol=XBTUSD&cache=7366225&theme=dark&locale=zh-CN&restart=0&origin=https://www.bitmex.com"

kfpth = '../../btc/bitmex/key.txt'

f = open(kfpth,'r')
lines = f.readlines()
f.close()

tid = lines[0].replace('\r','').replace('\n','')
key = lines[1].replace('\r','').replace('\n','')



