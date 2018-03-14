#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于访问OKCOIN 期货REST API
from bitmex_ws import BitMEXWebsocket

import logging
import os
import time
from magetool import timetool

kfpth = '../../../btc/bitmex/key.txt'



class klineTool:

    def __init__(self,apiconfpth = kfpth):
        
        f = open(apiconfpth,'r')
        lines = f.readlines()
        f.close()

        apikey = lines[0].replace('\r','').replace('\n','')
        secretkey = lines[1].replace('\r','').replace('\n','')

        # https://www.bitmex.com/realtime
        # https://www.bitmex.com/api/v1
        self.ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/realtime", symbol="XBTUSD",api_key=None, api_secret=None)

        # time.sleep(3)
        self.logger = self.setup_logger()

        # self.logger.info("Instrument data: %s" % self.ws.get_instrument())


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
   

    #OKCoin期货市场深度信息
    def future_depth(self,symbol,contractType,size): 
        if symbol == 'XBT':
            if contractType == 'XBTUSD':
                return self.future_depth_xbtusd(size)
            else:
                print('合约交易类型%s不可用:'%(contractType))

        else:
            print('市场类型%s不可用:'%(symbol))

        return None

    def future_depth_xbtusd(self,size):
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
            
            backsells = sells[:size]
            print(backsells)
            print('----------')
            buys.sort(reverse = True)
            backbuys = buys[:size]
            print(backbuys)
            return backbuys,backsells[::-1]
        else:
            print('websocket连接错误')
            # self.ws.ws.sock.connect()
            return None,None

    def getInstrument(self):
        self.ws.get_instrument()

    def getTicker(self):
        self.ws.get_ticker()


    def getQuoteBin1m(self):
        return self.ws.data['quoteBin1m']

    def getTradeBin1m(self):
        return self.ws.data['tradeBin1m']


    #清空100分钟前的数据
    def clearTradeBin1m(self):
        self.ws.data['tradeBin1m'] = []


def conventDataForSave(dat):
    # {'timestamp': '2018-03-14T15:17:00.000Z', 'symbol': 'XBTUSD', 'open': 8707.5, 'high': 8720, 'low': 8706, 'close': 8716.5, 'trades': 357, 'volume': 1488175, 'vwap': 8710.0427, 'lastSize': 500, 'turnover': 17086355694, 'homeNotional': 170.86355693999997, 'foreignNotional': 1488175},
    outs = []
    for d in dat:
        utctime = d['timestamp']
        timest = timetool.utcStrTimeToTime(utctime)
        timeint = int(timest)
        ltimeStr = timetool.timestamp2datetime(timest,True)
        opentmp = d['open']
        hithtmp = d['high']
        lowtmp = d['low']
        closetmp = d['close']
        volumetmp = d['volume']
        symboltmp = d['symbol']
        outs.append([timeint,opentmp,hithtmp,lowtmp,closetmp,volumetmp,symboltmp,str(ltimeStr)])
    return outs

def saveListWithLineTxt(datas,txtpth):
    ostr = ''
    for d in datas:
        ostr += str(d) + '\n'
    ostr = ostr[:-1]
    f = open(txtpth,'w')
    f.write(ostr)
    f.close()

def saveDataToFile(datas):
    strtoday = timetool.getDateDay()
    # strlastday = timetool.getLastDayDate(strtoday)
    todatpth = savedir + os.sep + strtoday
    if not os.path.exists(todatpth):
        os.mkdir(todatpth)
    loctim = time.localtime()
    hourtime = str(loctim.tm_hour) + '_' + str(loctim.tm_min) + '_' +  str(loctim.tm_sec)
    fpth = todatpth + os.sep + hourtime + '.txt'
    saveListWithLineTxt(datas, fpth)

def main():
    bittool = klineTool()
    savedir = 'out'
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    stime  = 0
    while True:
        stime += 1
        bin1m = bittool.getTradeBin1m()
        psavedats = conventDataForSave(bin1m)
        # [{'timestamp': '2018-03-14T15:17:00.000Z', 'symbol': 'XBTUSD', 'open': 8707.5, 'high': 8720, 'low': 8706, 'close': 8716.5, 'trades': 357, 'volume': 1488175, 'vwap': 8710.0427, 'lastSize': 500, 'turnover': 17086355694, 'homeNotional': 170.86355693999997, 'foreignNotional': 1488175}, {'timestamp': '2018-03-14T15:18:00.000Z', 'symbol': 'XBTUSD', 'open': 8716.5, 'high': 8717, 'low': 8696.5, 'close': 8697, 'trades': 365, 'volume': 1596155, 'vwap': 8710.0427, 'lastSize': 1999, 'turnover': 18326311630, 'homeNotional': 183.26311630000004, 'foreignNotional': 1596155}]
        # print(bin1m)
        print(len(bin1m))
        saveDataToFile(psavedats)
        bittool.clearTradeBin1m()
        time.sleep(3630)  #每小时取一次数据
        

def test():

    dt = '2018-03-14T15:03:00.000Z'
    print(timetool.utcStrTimeToTime(dt))

if __name__ == '__main__':
    main()




    
