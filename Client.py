#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

# from OkcoinSpotAPI import OKCoinSpot
# from OkcoinFutureAPI import OKCoinFuture
import bitmex
from magetool import urltool
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

# okcoinRESTURL = 'www.okex.com'#'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

def sayMsg(msg):
    cmd = 'say %s'%(msg)
    os.system(cmd)
    print msg


class TradeTool(object):
    """docstring for ClassName"""
    def __init__(self,amount = 30,isTest = False):
        self.okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
        self.depthSells = []
        self.depthBuys = []
        self.amount = amount
        self.isTest = isTest
        self.IDs = []
        self.isOpen = False

    def setAmount(self,amount):
        self.amount = amount

    def printSet(self):
        print 'isTest:',self.isTest
        print 'amount:',self.amount

    def getDepth(self):
        turl = 'https://www.okex.com/api/v1/future_depth.do?symbol=ltc_usd&contract_type=quarter&size=20'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        buys = ddic['bids']
        sells = ddic['asks']
        return buys,sells

    def getAllOrderIDs(self):
        #future_orderinfo(self,symbol,contractType,orderId,status,currentPage,pageLength)
        try:
            tmpjson = self.okcoinFuture.future_orderinfo('ltc_usd','quarter','-1','1','1','30')
            dic = json.loads(tmpjson)
            self.IDs = []
            for t in dic['orders']:
                self.IDs.append(t['order_id'])
        except Exception as e:
            print '请求合约信息出错:'
            print e
            self.IDs = []
        

    #1:开多   2:开空   3:平多   4:平空
    def openShort(self,ptype,pprice = None,pamount = None):



        if self.isOpen:
            instr = raw_input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            print instr
            if instr != 'y':
                print '已开仓，选择本次不开仓'
                return

        print ('期货开空单')

        tmpamount = self.amount

        if pprice and pamount:
            try:
                print '开空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'2','0','10')
                cmd = 'say 开空,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif pprice and not(pamount):
            try:
                print '开空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(self.amount),'2','0','10')
                cmd = 'say 开空,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)
            

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        # inputstr = raw_input("请输入：");
        # print inputstr
        inputstr = ptype
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None
        print inputidx,type(inputidx)

        
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
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1]

            self.isOpen = True

            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + 0.001
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'2','0','10')
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - 0.001
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'2','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '开空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'2','0','10')
            if tmpprice > 0:
                cmd = 'say 开空,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print '输入数据错误'

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
                print '平空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'4','0','10')
                cmd = 'say 平空,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif pprice and not(pamount):
            try:
                print '平空使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(self.amount),'4','0','10')
                cmd = 'say 平空,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        # inputstr = raw_input("请输入：");
        inputstr = ptype
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print ('期货平空单')
        
        if inputidx != None:
            self.depthBuys,self.depthSells = self.getDepth()
            atmp = list(self.depthSells)
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1]

            self.isOpen = False
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - 0.001
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'4','0','10')
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + 0.001
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'4','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '平空使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'4','0','10')
            if tmpprice > 0:
                cmd = 'say 平空,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print '输入数据错误'

    def openLong(self,ptype,pprice = None,pamount = None):
        if self.isOpen:
            instr = raw_input('已开发仓是否继续开%d个空仓(y/n):'%(self.amount))
            print instr
            if instr != 'y':
                print '已开仓，选择本次不开仓'
                return
        tmpamount = self.amount
        if pprice and pamount:
            try:
                print '开多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'1','0','10')
                cmd = 'say 开多,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif pprice and not(pamount):
            try:
                print '开多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(self.amount),'1','0','10')
                cmd = 'say 开多,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        # inputstr = raw_input("请输入：");
        inputstr = ptype
        print inputstr
        try:
            inputidx = int(inputstr)
        except Exception as e:
            inputidx = None

        print ('期货开多单')
        
        
        if inputidx != None:

            self.depthBuys,self.depthSells = self.getDepth()
            atmp = self.depthSells
            self.depthSells = self.depthBuys
            self.depthBuys = atmp
            tmps = self.depthBuys
            count = len(tmps)
            for p in tmps:
                print count,'\t',p[0],'\t',p[1]
                count -= 1
            print -1,'\t',self.depthSells[0][0],'\t',self.depthSells[0][1]

            self.isOpen = True
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[-1] 
                tmpprice = v[0] - 0.001
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'1','0','10')
            elif inputidx < 0:
                v = self.depthSells[0] 
                tmpprice = v[0] + 0.001
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'1','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '开多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'1','0','10')
            if tmpprice > 0:
                cmd = 'say 开多,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print '输入数据错误'
        

    def closeLong(self,ptype,pprice = None,pamount = None):

        print ('期货平多单')
        tmpamount = self.amount
        if pprice and pamount:
            try:
                print '平多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(pamount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(pamount),'3','0','10')
                cmd = 'say 平多,%.3f,%d张'%(float(pprice),int(pamount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif pprice and not(pamount):
            try:
                print '平多使用买一价下单:%.3f,amount:%d'%(float(pprice),int(self.amount))
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(pprice),str(self.amount),'3','0','10')
                cmd = 'say 平多,%.3f,%d张'%(float(pprice),int(self.amount))
                os.system(cmd)
            except Exception as e:
                cmd = 'say 参数错误'
                os.system(cmd)
                print '参数错误'
            return
        elif (not pprice) and pamount:
            tmpamount = int(pamount)

        outstr = '输入要下单的深度成交价编号\n>=1时,价格为深度编号\n0:价格为略高于买一价\n-1:'
        print outstr
        # inputstr = raw_input("请输入：");
        inputstr = ptype
        print inputstr
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
                print count,'\t',p[0],'\t',p[1]
                count -= 1

            print -1,'\t',self.depthSells[-1][0],'\t',self.depthSells[-1][1]

            self.isOpen = False
            tmpprice = 0.0
            if inputidx == 0:
                v = self.depthBuys[0]
                tmpprice = v[0] + 0.001
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'3','0','10')
            elif inputidx < 0:
                v = self.depthSells[-1] 
                tmpprice = v[0] - 0.001
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'3','0','10')
            elif inputidx > 0:
                tmps = tmps[::-1]
                v = tmps[inputidx - 1]
                tmpprice = v[0]
                print '平多使用买一价下单:%.3f,amount:%d'%(tmpprice,tmpamount)
                if not self.isTest:
                    print self.okcoinFuture.future_trade('ltc_usd','quarter',str(tmpprice),str(tmpamount),'3','0','10')
            if tmpprice > 0:
                cmd = 'say 平多,%.3f,%d张'%(tmpprice,tmpamount)
                os.system(cmd)
        else:
            print '输入数据错误'

    def cleanAllTrade(self):
        self.getAllOrderIDs()
        time.sleep(0.1)
        if self.IDs:
            strids = self.IDs[0]
            if len(self.IDs) > 1:
                idstmp = []
                for i in self.IDs:
                    idstmp.append(str(i))
                strids = ','.join(idstmp)
            print self.okcoinFuture.future_cancel('ltc_usd','quarter',strids)
            print '所有定单已取消'
        self.isOpen = False

# print ('期货下单')
# print (okcoinFuture.future_trade('ltc_usd','quarter','147.205','30','1','0','10'))

#print (u'期货批量下单')
#print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))

#print (u'期货取消订单')
#print (okcoinFuture.future_cancel('ltc_usd','this_week','47231499'))

#print (u'期货获取订单信息')
# jsonstr =  (okcoinFuture.future_orderinfo('ltc_usd','quarter','-1','2','1','30'))

# print jsonstr

# outsrt = json.dumps(jsonstr)

# print(outsrt)

#print (u'期货逐仓账户信息')
#print (okcoinFuture.future_userinfo_4fix())

#print (u'期货逐仓持仓信息')
#print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))

def main(pAmount = 30, ispTest = True):
     tradetool = TradeTool(amount = pAmount,isTest = ispTest)
     pstr = '程序重新运行,\nos:开空\ncs:平空\nol:开多\ncl:平多\np:输出设置项\nset:设置每次成交量\nc:取消所有未成交定单\ntest:\n\t输入1表示使用测试方式运行\n\t0表示正试运行下单\nq:退出\n请输入:'
     while True:
        inputstr = raw_input(pstr);
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
                print '开仓量改为:%d'%(intam)
            except Exception as e:
                print '输入参数错误,请输入要设置的下单数量,(set 下单数量)'
        elif inputstr == 'q':
            print '程序退出成功'
            break
        elif inputstr == 'c':
            tradetool.cleanAllTrade()
        elif inputstr == 'p':
            tradetool.printSet()
        elif inputstr == 'test':
            if len(inputstrs) == 2:
                if inputstrs[1] == '1':
                    tradetool.isTest = True
                    print '开启下单测试,isTest = ',tradetool.isTest
                elif inputstrs[1] == '0':
                    tradetool.isTest = False
                    print '关闭下单测试,isTest = ',tradetool.isTest
                else:
                    sayMsg('输入参数错误')
                    print '输入参数错误'
            else:
                tradetool.isTest = True
                print '开启下单测试,isTest = ',tradetool.isTest
        else:
            print '输入错误，%s'%(pstr)

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        amount = int(args[1])
        if amount:
            main(pAmount = amount)
        elif args[1] == 'test': 
            print 'a程序使用测试方式运行\nmount未设置,使用默认值:30\n可在程序中重新设置\n，'
            main(ispTest = False)
    else:
        print '程序只接受一个参数,test或者下单数量'
   
