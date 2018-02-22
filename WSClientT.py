#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from bitmex_websocket import BitMEXWebsocket
import logging

import threading

# import Queue

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

# Basic use of websocket.

class DepthGetObj(object):
    """docstring for DepthGetObj"""
    def __init__(self, isGetDep):
        self.isGetDep = isGetDep

depobj = DepthGetObj(False)


class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self,cond):
        threading.Thread.__init__(self)
        self.cond = cond
        self.ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD",api_key=None, api_secret=None)

        self.logger = self.setup_logger()

        self.logger.info("Instrument data: %s" % self.ws.get_instrument())

    def getDepth(self):
        if self.ws.ws.sock.connected:
            depthdat = self.ws.market_depth()
        # logger.info("Market Depth: %s" % depthdat)
            print(type(depthdat),len(depthdat))
            sells = []
            buys = []
            for d in depthdat:
                if d['symbol'] == 'XBTUSD':
                    if d['side'] == 'Buy':
                        buys.append([d['price'],d['size']])
                    elif d['side'] == 'Sell':
                        sells.append([d['price'],d['size']])
            sells.sort()
            print(sells[:5])
            print('----------')
            buys.sort(reverse = True)
            print(buys[:5])

    def run(self):

        # Run forever
        while True:

            self.cond.clear()
            self.cond.wait()

            time.sleep(0.5)


    def setup_logger(self):
        # Prints logger info to terminal
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
        ch = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

# import threading, time
class Hider(threading.Thread):
    def __init__(self, cond, name):
        super(Hider, self).__init__()
        self.cond = cond
        self.name = name
        self.dat = '0'
    
    def setDat(self,dats):
        self.dat = dats
        self.cond.set()

    def run(self):
        time.sleep(1) #确保先运行Seeker中的方法   
        print('xxx1')
        while True:
            print('while start')
            self.cond.clear()
            self.cond.wait() #c    
            print(self.dat)
            print('while end')


  
def main():      
    # cond = threading.Condition()
    cond = threading.Event()
    # hider = Hider(cond, 'hider')
    hider = WorkerThread(cond)
    hider.setDaemon(True)
    hider.start()
    while True:
        instr = input('输入参数')
        print(instr,type(instr))
        if instr == '1' or instr == 1:
            # cond.acquire() #b    #加锁
            print('input 1')
            # hider.setDat(str(instr))
            hider.getDepth()
        time.sleep(1)    

# def main():
#     downthread = WorkerThread()
#     downthread.setDaemon(True)
#     downthread.start()

#     while True:
#         instr = input('输入参数')
#         if instr == '1':
#             depobj.isGetDep = True
#         time.sleep(1)

if __name__ == "__main__":
    main()


   
