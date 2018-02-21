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
    def __init__(self,isTest = True):
        self.okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
        self.depthSells = []
        self.depthBuys = []
        self.isOpne = False
        self.isTest = isTest


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
        self.isOpne = True
        if self.isTest:
            print 'test openshort:price=%.3f,amount=%d'%(pprice,pamount)
        else:
            print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'2','0','10')
        

    def closeShort(self,pprice,pamount):
        print ('期货平空')
        print time.ctime()
        self.isOpne = False
        if self.isTest:
            print 'test closeShort:price=%.3f,amount=%d'%(pprice,pamount)
        else:
            print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'4','0','10')
                

    def openLong(self,pprice,pamount):
        print ('期货开多')
        print time.ctime()
        self.isOpne = True
        if self.isTest:
            print 'test openLong:price=%.3f,amount=%d'%(pprice,pamount)
        else:
            print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'1','0','10')

    def closeLong(self,pprice,pamount):

        print ('期货平多')
        self.isOpne = False
        if self.isTest:
            print 'test closeLong:price=%.3f,amount=%d'%(pprice,pamount)
        else:
            print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'3','0','10')
        
#up
testBS = [(100,101),(110,111),(120,121),(130,131),(140,141),(150,151)]
#down
testBS = testBS[::-1]
testCount = [0]
def getBuyAndSell(tradetool):
    if tradetool.isTest:
        if testCount[0] == len(testBS):
            return None,None
        back = testBS[testCount[0]]
        testCount[0] += 1
        return back
    else:
        try:
            bs,ss = tradetool.getDepth()
            ss = ss[::-1]
            return bs[0][0],ss[0][0]
        except Exception as e:
            return None,None
    


def main(openprice,closeprice,stopprice,amount,pIsTest = False):

    tradetool = TradeTool(pIsTest)
    print 'is run'
    tradetool.isOpne = False
    while True:
        b = None
        s = None
        if not tradetool.isOpne:
            if openprice > closeprice: #开空单
                print '开空'
                b,s = getBuyAndSell(tradetool)
                print b,s,openprice
                if b != None and b > openprice:
                    try:
                        print '开空1'
                        tradetool.openShort(openprice,amount)
                    except Exception as e:
                        print 'openShort erro'
            else: #开多单
                print '开多'
                b,s = getBuyAndSell(tradetool)
                print b,s,openprice
                if s != None and s < openprice:
                    try:
                        print '开多1'
                        tradetool.openLong(openprice,amount)
                    except Exception as e:
                        print 'openLong erro'
        else:
            if openprice > closeprice: #开空单,平空
                print '平空'
                b,s = getBuyAndSell(tradetool)
                #止盈
                if s != None and s < closeprice:
                    try:
                        print '平空1'
                        tradetool.closeShort(closeprice,amount)
                        break
                    except Exception as e:
                        print 'closeshort erro'
                elif s != None and s > stopprice:
                    try:
                        print '平空2'
                        tradetool.closeShort(stopprice,amount)
                        break
                    except Exception as e:
                        print 'closeshort erro'
            else:#开多单，平多
                print '平多'
                b,s = getBuyAndSell(tradetool)
                if b != None and b > closeprice:
                    try:
                        print '平多1'
                        tradetool.closeLong(closeprice,amount)
                        break
                    except Exception as e:
                        print 'closelong erro'
                elif b != None and b < stopprice:
                    try:
                        print '平多2'
                        tradetool.closeLong(stopprice,amount)
                        break
                    except Exception as e:
                        print 'closelong erro'
            
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
    if len(args) == 5:
        oprice = float(args[1])
        cprice = float(args[2])
        sprice = float(args[3])
        amount = int(args[4])
        print(oprice,cprice,sprice,amount)
        if oprice > cprice and sprice < oprice:
            print '开空单止损价要大开开单价'
        elif oprice < cprice and sprice > oprice:
            print '开多单止损价要小于开单价'
        elif oprice and cprice and sprice and amount:
            main(oprice,cprice,sprice,amount)
        else: 
            test()
            print '参数错误，要输入止损类型，数量和价格' 
    else:
        test()
        print '参数错误，要输入止损类型，数量和价格' 
   
