#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
from magetool import urltool
import json
import sys
import os
import time

f = open('../../btc/okexapikey/okexapikey.txt','r')
tmpstr = f.read()
f.close()

apikeydic = json.loads(tmpstr)

#初始化apikey，secretkey,url
apikey = apikeydic['apikey']
secretkey = apikeydic['secretkey']
okcoinRESTURL = 'www.okex.com'#'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

def sayMsg(msg):
    cmd = 'say %s'%(msg)
    os.system(cmd)
    print msg


class TradeTool(object):
    """docstring for ClassName"""
    def __init__(self):
        self.okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
        self.depthSells = []
        self.depthBuys = []


    def getDepth(self):
        turl = 'https://www.okex.com/api/v1/future_depth.do?symbol=ltc_usd&contract_type=quarter&size=20'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        buys = ddic['bids']
        sells = ddic['asks']
        return buys,sells
        

    #1:开多   2:开空   3:平多   4:平空
    def openShort(self,pprice,pamount):

        print ('期货开空')
        print time.ctime()
        print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'2','0','10')
        

    def closeShort(self,pprice,pamount):
        print ('期货平空')
        print time.ctime()
        print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'4','0','10')
                

    def openLong(self,pprice,pamount):
        print ('期货开多')
        print time.ctime()
        print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'1','0','10')

    def closeLong(self,pprice,pamount):

        print ('期货平多')
        print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'3','0','10')
        

def getBuyAndSell(tradetool):
    try:
        bs,ss = tradetool.getDepth()
        ss = ss[::-1]
        return bs[0][0],ss[0][0]
    except Exception as e:
        return None,None
    


def main(ptype,cprice,amount):
     tradetool = TradeTool()
     print 'is run'
     while True:
        b = None
        s = None
        if ptype == 'cl':
            b,s = getBuyAndSell(tradetool)
            if b and b > cprice:
                try:
                    tradetool.closeLong(cprice,amount)
                    break
                except Exception as e:
                    print 'closelong erro'
        elif ptype == 'cs':
            b,s = getBuyAndSell(tradetool)
            if s and s < cprice:
                try:
                    tradetool.closeShort(cprice,amount)
                    break
                except Exception as e:
                    print 'closeshort erro'
        else:
            print 'b=',b,',s=',s,',time=',time.ctime

        time.sleep(300) #5分钟测一次止损价
        
        
def test():
    tradetool = TradeTool()
    bs,ss = tradetool.getDepth()
    ss = ss[::-1]
    for s in ss:
        print s
    print '------'
    for b in bs:
        print b
    print getBuyAndSell(tradetool)
if __name__ == '__main__':
    args = sys.argv
    if len(args) == 4:
        ptype = args[1]
        cprice = args[2]
        camount = args[3]
        print(ptype,cprice,camount)
        if ptype and cprice and camount:
            main(ptype,cprice,amount)
        else: 
            test()
            print '参数错误，要输入止损类型，数量和价格' 
    else:
        test()
        print '参数错误，要输入止损类型，数量和价格' 
   
