#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

import bitmex
import inspect
# from magetool import urltool
import json
import sys
import os
import time

kfpth = '../../btc/bitmex/key.txt'

f = open(kfpth,'r')
lines = f.readlines()
f.close()

apikey = lines[0].replace('\r','').replace('\n','')
secretkey = lines[1].replace('\r','').replace('\n','')

client = bitmex.bitmex(test=False, api_key=apikey, api_secret=secretkey)



#开多
# res = client.Order.Order_new(symbol='XBTUSD', orderQty=1, price=11030.0).result()
# print(res)
#平多

# res = client.Order.Order_new(symbol='XBTUSD', orderQty=1,execInst='Close', price=11030.0).result()
# print(res)

# res = client.Order.Order_closePosition(symbol='XBTUSD',price=11030.0).result()
# print(res)

#开空
# res = client.Order.Order_new(symbol='XBTUSD', orderQty=-1, price=11040.0).result()
# print(res)
# # #平空
# res = client.Order.Order_closePosition(symbol='XBTUSD',price=11038.0).result()
# print(res)

# def f(a,b,c):
#     pass
# print(f.__code__.co_varnames)

# print(dir(client.Order.Order_closePosition))
# print(type(client.Order.Order_closePosition.operation))
# print(dir(client.Order.Order_closePosition.operation))
# print(repr(client.Order.Order_closePosition.operation))
# print(client.Order.Order_closePosition.operation.params)
# print('--------------------------')
# print(client.Order.Order_new.operation.params)

# res = client.Instrument.Instrument_get(filter=json.dumps({'rootSymbol': 'XBT'})).result()
# print(res)
# print(dir(client.Order))
# res = client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()
# print(res)
