#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果
import threading
import sys
import os
import time


class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self,ws,priceAlarm):
        threading.Thread.__init__(self)

        self.ws = ws
        self.alarmPrice = None
        self.alarmType = -3   #0,默认，1，上涨预警，-1，下跌预警,-2，未设置

        self.cond = threading.Event()

        
        self.alarmDelay = 5 #每5秒钟检测一次当前价格
        self.timeinit = 60  #60x5=300,即每5分钟显示一次当前价格

        self.timeCount = self.timeinit

        self.alarmCount = 0  #50秒报一次

    
        if priceAlarm != None:
            self.startAlarm(priceAlarm)
        else:
            self.stopAlarm()

    def getDepth(self):
        if self.ws.ws.sock.connected:
            depthdat = self.ws.market_depth()
        # logger.info("Market Depth: %s" % depthdat)
            # print(type(depthdat),len(depthdat))
            sells = []
            buys = []
            for d in depthdat:
                if d['symbol'] == 'XBTUSD':
                    if d['side'] == 'Buy':
                        buys.append([d['price'],d['size']])
                    elif d['side'] == 'Sell':
                        sells.append([d['price'],d['size']])
            sells.sort()
            buys.sort(reverse = True)
            return float(buys[0][0]),float(sells[0][0])
    def __isAlarm(self,isShow = False):
            bs = self.getDepth()
            if bs != None:
                if self.alarmType == 0 and self.alarmPrice >= bs[0] and self.alarmPrice <= bs[1]:
                    print(bs[0],bs[1],self.alarmPrice)
                    return True
                elif self.alarmType == 1 and self.alarmPrice <= bs[0]:
                    print(bs[0],bs[1],self.alarmPrice)
                    return True
                elif self.alarmType == -1 and self.alarmPrice >= bs[1]:
                    print(bs[0],bs[1],self.alarmPrice)
                    return True
                else:
                    if self.timeCount <= 0 or isShow:
                        self.timeCount = self.timeinit
                        print(bs[0],bs[1],self.alarmPrice)
                    return None
            return None

    def isWork(self):
        if self.cond.isSet():
            self.__isAlarm(isShow = True)
            return self.alarmPrice,self.alarmType
        else:
            return None

    def stopAlarm(self):
        self.cond.clear()
    def startAlarm(self,alarmPrice):
        self.alarmPrice = float(alarmPrice)
        self.timeCount = self.timeinit

        bs = self.getDepth()
        if self.alarmPrice >= bs[0] and self.alarmPrice <= bs[1]:
            self.alarmType = 0
        elif self.alarmPrice > bs[1]:
            self.alarmType = 1
        elif self.alarmPrice < bs[0]:
            self.alarmType = -1
        else:
            self.alarmType = -2
        print(bs,self.alarmPrice,self.alarmType)
        self.cond.set()
    def run(self):

        # Run forever
        while True:
            self.cond.wait() #c  
            if self.__isAlarm() != None:
                self.alarmCount -= 1
                if self.alarmCount <= 0:
                    cmd = ''
                    if self.alarmType == 0:
                        cmd = 'say 请注意，价格已达到%.1f'%(self.alarmPrice)
                    elif self.alarmType == 1:
                        cmd = 'say 请注意，价格上涨到%.1f'%(self.alarmPrice)
                    elif self.alarmType == -1:
                        cmd = 'say 请注意，价格下跌到%.1f'%(self.alarmPrice)
                    os.system(cmd)
                    self.alarmCount = self.timeinit/6

            time.sleep(self.alarmDelay)
            self.timeCount -= 1


class AlarmObj(object):
    """docstring for AlarmObj"""
    def __init__(self):
        super(AlarmObj, self).__init__()
        self.alarmT = None
        self.isInit = False
        
    def initAlarm(self,ws,price):
        if not self.isInit:
            self.alarmT = WorkerThread(ws, price)
            self.alarmT.setDaemon(True)
            self.alarmT.start()
            self.isInit = True
    def isWorked(self):
        return self.alarmT.isWork()

    def stopAlarm(self):
        self.alarmT.stopAlarm()

    def startAlarm(self,price):
        self.alarmT.startAlarm(price)

alarmobj = AlarmObj()

def initAlarmObj(ws):
    alarmobj.initAlarm(ws, None)

def startAlarm(price):
    alarmobj.startAlarm(price)

def stopAlarm():
    alarmobj.stopAlarm()

def isWork():
    return alarmobj.isWorked()
    
def main():      
    pass

if __name__ == "__main__":
    main()


   
