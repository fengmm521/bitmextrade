#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

# from OkcoinSpotAPI import OKCoinSpot
# from OkcoinFutureAPI import OKCoinFuture
import FutureAPI
import json
import sys
import os
import time


# okcoinRESTURL = 'www.okex.com'#'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

def sayMsg(msg):
    cmd = 'say %s'%(msg)
    os.system(cmd)
    print(msg)


class TradeTool(object):
    """docstring for ClassName"""
    def __init__(self,amount = 30,isTest = False,symbol = 'XBT',contractType = 'XBTUSD'):

        self.symbol = symbol
        self.contractType = contractType

        self.okcoinFuture = FutureAPI.Future()
        self.depthSells = []
        self.depthBuys = []
        self.amount = amount
        self.isTest = isTest
        self.IDs = []
        self.isOpen = False


        self.priceOffset = 0.5 #bitmex单价为0.5美元,okex单价为0.001美元

    def setAmount(self,amount):
        self.amount = amount

    def setAlarmPrice(self,price):
        self.okcoinFuture.startAlarm(price)
    def cleanAlarmPrice(self):
        self.okcoinFuture.stopAlarm()

    def printSet(self):
        print('isTest:',self.isTest)
        print('amount:',self.amount)
        alarmPrice = self.okcoinFuture.isAlarmWork()
        if alarmPrice != None:
            print('alarm:',alarmPrice)

    def getDepth(self):
        print(self.symbol,self.contractType)
        b,s = self.okcoinFuture.future_depth(self.symbol,self.contractType,size = 5)
        return b,s

    def getAllOrderIDs(self):
        return None

    #1:开多   2:开空   3:平多   4:平空
    def openShort(self,ptype,pprice = None,pamount = None):



        if self.isOpen:
            instr = input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            instr = str(instr)
            print(instr)
            if instr != 'y':
                print('已开仓，选择本次不开仓')
                return

        print('期货开空单')

        tmpamount = self.amount

        if pprice and pamount:
            try:
                print('开空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(pamount),'2','0','10'))
                cmd = 'say 开空,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif pprice and not(pamount):
            try:
                print('开空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(self.amount),'2','0','10'))
                cmd = 'say 开空,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)
            

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print(outstr)
        inputstr = ptype
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None
        print(inputidx,type(inputidx))

        
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            tmps = self.depthBuys[::-1]
            count = len(tmps)
            for p in tmps:
                print(count,'\t',p[0],'\t',p[1])
                count -= 1
            print(-1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1])

            self.isOpen = True

            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + self.priceOffset
                print('开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'2','0','10'))
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - self.priceOffset
                print('开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'2','0','10'))
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print('开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'2','0','10'))
            if tmpprice > 0:
                cmd = 'say 开空,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print('输入数据错误')

    def closeShort(self,ptype,pprice = None,pamount = None):
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10
        tmpamount = self.amount
        if pprice and pamount:
            try:
                print('平空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(pamount),'4','0','10'))
                cmd = 'say 平空,%.3f,%d张'%(float(pprice),int(pamount))
                self.isOpen = False
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif pprice and not(pamount):
            try:
                print('平空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(self.amount),'4','0','10'))
                cmd = 'say 平空,%.3f,%d张'%(float(pprice),int(self.amount))
                self.isOpen = False
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print(outstr)
        inputstr = ptype
        print(inputstr)
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print('期货平空单')
        
        if inputidx != None:
            self.depthBuys,self.depthSells = self.getDepth()
            atmp = list(self.depthSells)
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print(count,'\t',p[0],'\t',p[1])
                count -= 1
            print(-1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1])

            self.isOpen = False
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - self.priceOffset
                print('平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'4','0','10'))
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + self.priceOffset
                print('平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'4','0','10'))
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print('平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'4','0','10'))
            if tmpprice > 0:
                cmd = 'say 平空,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print('输入数据错误')

    def openLong(self,ptype,pprice = None,pamount = None):
        if self.isOpen:
            instr = input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            instr = str(instr)
            print(instr)
            if instr != 'y':
                print('已开仓，选择本次不开仓')
                return
        tmpamount = self.amount
        if pprice and pamount:
            try:
                print('开多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(pamount),'1','0','10'))
                cmd = 'say 开多,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif pprice and not(pamount):
            try:
                print('开多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(self.amount),'1','0','10'))
                cmd = 'say 开多,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print(outstr)
        inputstr = ptype
        print(inputstr)
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print('期货开多单')
        
        
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            atmp = self.depthSells
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print(count,'\t',p[0],'\t',p[1])
                count -= 1
            print(-1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1])

            self.isOpen = True
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - self.priceOffset
                print('开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'1','0','10'))
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + self.priceOffset
                print('开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'1','0','10'))
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print('开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'1','0','10'))
            if tmpprice > 0:
                cmd = 'say 开多,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print('输入数据错误')
        

    def closeLong(self,ptype,pprice = None,pamount = None):

        print('期货平多单')
        tmpamount = self.amount
        if pprice and pamount:
            try:
                print('平多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(pamount),'3','0','10'))
                cmd = 'say 平多,%.3f,%d张'%(float(pprice),int(pamount))
                self.isOpen = False
                os.system(cmd)
                
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif pprice and not(pamount):
            try:
                print('平多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount)))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(pprice),str(self.amount),'3','0','10'))
                cmd = 'say 平多,%.3f,%d张'%(float(pprice),int(self.amount))
                self.isOpen = False
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print('参数错误')
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print(outstr)
        inputstr = ptype
        print(inputstr)
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        
        # symbol String 是 btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        # contract_type String 是 合约类型: this_week:当周   next_week:下周   quarter:季度
        # api_key String 是 用户申请的apiKey 
        # sign String 是 请求参数的签名
        # price String 是 价格
        # amount String 是 委托数量
        # type String 是 1:开多   2:开空   3:平多   4:平空
        # match_price String 否 是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        # lever_rate String 否
        # 杠杆倍数 value:10\20 默认10
        
        
        # tmps = tmps[::-1]
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            tmps = self.depthBuys[::-1]
            count = len(tmps)
            for p in tmps:
                print(count,'\t',p[0],'\t',p[1])
                count -= 1

            print(-1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1])

            self.isOpen = False
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + self.priceOffset
                print('平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'3','0','10'))
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - self.priceOffset
                print('平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'3','0','10'))
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print('平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount))
                if not self.isTest:
                    print(self.okcoinFuture.future_trade(self.symbol,self.contractType,str(tmpprice),str(tmpamount),'3','0','10'))
            if tmpprice > 0:
                cmd = 'say 平多,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print('输入数据错误')

    def cleanAllTrade(self):
        time.sleep(0.1)
        self.okcoinFuture.future_cancel(self.symbol,self.contractType,None)
        self.isOpen = False


def main(pAmount = 100, ispTest = False):
     tradetool = TradeTool(amount = pAmount,isTest = ispTest)
     pstr = '程序重新运行,\nos:开空\ncs:平空\nol:开多\ncl:平多\np:输出设置项\nset:设置每次成交量\na:设置和取消价格报警\nc:取消所有未成交定单\ntest:\n\t输入1表示使用测试方式运行\n\t0表示正试运行下单\nq:退出\n请输入:'
     while True:
        inputstr = input(pstr);
        inputstr = str(inputstr)
        inputstr = inputstr.replace('\t','')
        inputstr = inputstr.replace('\n','')
        inputstr = ' '.join(inputstr.split())
        inputstrs = inputstr.split(' ')
        inputstr = inputstrs[0]
        if inputstr == 'os':
            if len(inputstrs) == 2:
                tradetool.openShort(inputstrs[1])
            elif len(inputstrs) == 3:
                if inputstrs[1] == '-p':
                    tradetool.openShort(-1,inputstrs[2])
                elif inputstrs[1] == '-a':
                    tradetool.openShort(-1,None,inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 4:
                if inputstrs[2] == '-a':
                    tradetool.openShort(inputstrs[1],None,inputstrs[3])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 5:
                if inputstrs[1] == '-p' and inputstrs[3] == '-a':
                    tradetool.openShort(-1,inputstrs[2],inputstrs[4])
                elif inputstrs[1] == '-a' and inputstrs[3] == '-p':
                    tradetool.openShort(-1,inputstrs[4],inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            else:
                tradetool.openShort('-1')
        elif inputstr == 'cs':
            if len(inputstrs) == 2:
                tradetool.closeShort(inputstrs[1])
            elif len(inputstrs) == 3:
                if inputstrs[1] == '-p':
                    tradetool.closeShort(-1,inputstrs[2])
                elif inputstrs[1] == '-a':
                    tradetool.closeShort(-1,None,inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 4:
                if inputstrs[2] == '-a':
                    tradetool.closeShort(inputstrs[1],None,inputstrs[3])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 5:
                if inputstrs[1] == '-p' and inputstrs[3] == '-a':
                    tradetool.closeShort(-1,inputstrs[2],inputstrs[4])
                elif inputstrs[1] == '-a' and inputstrs[3] == '-p':
                    tradetool.closeShort(-1,inputstrs[4],inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            else:
                tradetool.closeShort('-1')
        elif inputstr == 'ol':
            if len(inputstrs) == 2:
                tradetool.openLong(inputstrs[1])
            elif len(inputstrs) == 3:
                if inputstrs[1] == '-p':
                    tradetool.openLong(-1,inputstrs[2])
                elif inputstrs[1] == '-a':
                    tradetool.openLong(-1,None,inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 4:
                if inputstrs[2] == '-a':
                    tradetool.openLong(inputstrs[1],None,inputstrs[3])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 5:
                if inputstrs[1] == '-p' and inputstrs[3] == '-a':
                    tradetool.openLong(-1,inputstrs[2],inputstrs[4])
                elif inputstrs[1] == '-a' and inputstrs[3] == '-p':
                    tradetool.openLong(-1,inputstrs[4],inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            else:
                tradetool.openLong('-1')
        elif inputstr == 'cl':
            if len(inputstrs) == 2:
                tradetool.closeLong(inputstrs[1])
            elif len(inputstrs) == 3:
                if inputstrs[1] == '-p':
                    tradetool.closeLong(-1,inputstrs[2])
                elif inputstrs[1] == '-a':
                    tradetool.closeLong(-1,None,inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 4:
                if inputstrs[2] == '-a':
                    tradetool.closeLong(inputstrs[1],None,inputstrs[3])
                else:
                    sayMsg('输入参数错误')
            elif len(inputstrs) == 5:
                if inputstrs[1] == '-p' and inputstrs[3] == '-a':
                    tradetool.closeLong(-1,inputstrs[2],inputstrs[4])
                elif inputstrs[1] == '-a' and inputstrs[3] == '-p':
                    tradetool.closeLong(-1,inputstrs[4],inputstrs[2])
                else:
                    sayMsg('输入参数错误')
            else:
                tradetool.closeLong('-1')
        elif inputstr == 'set' and len(inputstrs) == 2:
            try:
                intam = int(inputstrs[1])
                tradetool.amount = intam
                print('开仓量改为:%d'%(intam))
            except Exception as e:
                print('输入参数错误,请输入要设置的下单数量,(set 下单数量)')
        elif inputstr == 'q':
            print('程序退出成功')
            break
        elif inputstr == 'c':
            tradetool.cleanAllTrade()
        elif inputstr == 'p':
            tradetool.printSet()
        elif inputstr == 'a':
            if len(inputstrs) == 2:
                try:
                    tmpprice = float(inputstrs[1])
                    tradetool.setAlarmPrice(tmpprice)
                except Exception as e:
                    tradetool.cleanAlarmPrice()
            else:
                tradetool.cleanAlarmPrice()
        elif inputstr == 'test':
            if len(inputstrs) == 2:
                if inputstrs[1] == '1':
                    tradetool.isTest = True
                    print('开启下单测试,isTest = ',tradetool.isTest)
                elif inputstrs[1] == '0':
                    tradetool.isTest = False
                    print('关闭下单测试,isTest = ',tradetool.isTest)
                else:
                    sayMsg('输入参数错误')
                    print('输入参数错误')
            else:
                tradetool.isTest = True
                print('开启下单测试,isTest = ',tradetool.isTest)
        else:
            print('输入错误，%s'%(pstr))

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        amount = int(args[1])
        if amount:
            main(pAmount = amount)
        elif args[1] == 'test': 
            print('a程序使用测试方式运行\nmount未设置,使用默认值:30\n可在程序中重新设置\n，')
            main(ispTest = False)
    else:
        print('程序只接受一个参数,test或者下单数量')
   
