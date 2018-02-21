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
    def __init__(self):
        threading.Thread.__init__(self)

    def stop(self):
        pass

    def run(self):

        logger = self.setup_logger()

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
        ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD",
                             api_key=None, api_secret=None)

        logger.info("Instrument data: %s" % ws.get_instrument())

        # Run forever
        while(ws.ws.sock.connected):
            # logger.info("Ticker: %s" % ws.get_ticker())
            # if ws.api_key:
            #     logger.info("Funds: %s" % ws.funds())
            # logger.info("Market Depth: %s" % ws.market_depth())
            # logger.info("Recent Trades: %s\n\n" % ws.recent_trades())
            # sleep(10)
            if depobj.isGetDep:
                depthdat = ws.market_depth()
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
                depobj.isGetDep = False
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

def main():
    downthread = WorkerThread()
    downthread.setDaemon(True)
    downthread.start()

    while True:
        instr = input('输入参数')
        if instr == '1':
            depobj.isGetDep = True
        time.sleep(1)

if __name__ == "__main__":
    main()


   
