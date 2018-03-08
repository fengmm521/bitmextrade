#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于访问OKCOIN 期货REST API
from bitmex_websocket import BitMEXWebsocket

import bitmex
import logging

import AlarmPrice

kfpth = '../../btc/bitmex/key.txt'



class Future:

    def __init__(self,apiconfpth = kfpth):
        
        f = open(apiconfpth,'r')
        lines = f.readlines()
        f.close()

        apikey = lines[0].replace('\r','').replace('\n','')
        secretkey = lines[1].replace('\r','').replace('\n','')

        self.client = bitmex.bitmex(test=False, api_key=apikey, api_secret=secretkey)
        # www.bitmex.com/realtime
        # https://www.bitmex.com/api/v1
        self.ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/realtime", symbol="XBTUSD",api_key=None, api_secret=None)

        self.logger = self.setup_logger()

        self.logger.info("Instrument data: %s" % self.ws.get_instrument())

        AlarmPrice.initAlarmObj(self.ws)
        
    def startAlarm(self,price):
        AlarmPrice.startAlarm(price)

    def stopAlarm(self):
        AlarmPrice.stopAlarm()

    def isAlarmWork(self):
        return AlarmPrice.isWork()

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
    #期货下单
    def future_trade(self,symbol,contractType,price='',amount='',tradeType='',matchPrice='',leverRate=''):
        
        if symbol == 'XBT':
            if contractType == 'XBTUSD':
                return self.future_trade_xbtusd(price, amount, tradeType)
            else:
                print('合约交易类型%s不可用:'%(contractType))

        else:
            print('市场类型%s不可用:'%(symbol))

        res = None

        return res

    def future_trade_xbtusd(self,price,amount,tradeType):
        res = None
        tmpprice = '%.1f'%(float(price))
        if tradeType == '1': #开多
            print('开多:',tmpprice,amount)
            res = self.client.Order.Order_new(symbol='XBTUSD', orderQty=int(amount), price=float(tmpprice)).result()
        elif tradeType == '3': #平多
            print('平多:',tmpprice,amount)
            res = self.client.Order.Order_new(symbol='XBTUSD', orderQty=-int(amount),execInst='Close', price=float(tmpprice)).result()
        elif tradeType == '2': #开空
            print('开空:',tmpprice,amount)
            res = self.client.Order.Order_new(symbol='XBTUSD', orderQty=-int(amount), price=float(tmpprice)).result()
        elif tradeType == '4': #平空
            print('平空:',tmpprice,amount)
            res = self.client.Order.Order_new(symbol='XBTUSD', orderQty=int(amount),execInst='Close', price=float(tmpprice)).result()
        else:
            print('tradeType,下单类型设置错误:',tradeType)

        return res[0]

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

    #期货取消所有定单订单
    def future_cancel(self,symbol,contractType,orderId):
        res = None
        if orderId == '' or (not orderId):
            res = self.client.Order.Order_cancelAll().result()
            print(res)
        else:
            res = self.client.Order.Order_cancel(orderId).result()
            print(res)
        return res

    #期货获取订单信息
    def future_orderinfo(self,symbol,contractType,orderId,status,currentPage,pageLength):
        pass
        # FUTURE_ORDERINFO = "/api/v1/future_order_info.do?"
        # params = {
        #     'api_key':self.__apikey,
        #     'symbol':symbol,
        #     'contract_type':contractType,
        #     'order_id':orderId,
        #     'status':status,
        #     'current_page':currentPage,
        #     'page_length':pageLength
        # }
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_ORDERINFO,params)

#-------------
    #OKCOIN期货行情信息
    def future_ticker(self,symbol,contractType):
        pass
        # FUTURE_TICKER_RESOURCE = "/api/v1/future_ticker.do"
        # params = ''
        # if symbol:
        #     params += '&symbol=' + symbol if params else 'symbol=' +symbol
        # if contractType:
        #     params += '&contract_type=' + contractType if params else 'contract_type=' +symbol
        # return httpGet(self.__url,FUTURE_TICKER_RESOURCE,params)

    

    #OKCoin期货交易记录信息
    def future_trades(self,symbol,contractType):
        pass
        # FUTURE_TRADES_RESOURCE = "/api/v1/future_trades.do"
        # params = ''
        # if symbol:
        #     params += '&symbol=' + symbol if params else 'symbol=' +symbol
        # if contractType:
        #     params += '&contract_type=' + contractType if params else 'contract_type=' +symbol
        # return httpGet(self.__url,FUTURE_TRADES_RESOURCE,params)

    #OKCoin期货指数
    def future_index(self,symbol):
        pass
        # FUTURE_INDEX = "/api/v1/future_index.do"
        # params=''
        # if symbol:
        #     params = 'symbol=' +symbol
        # return httpGet(self.__url,FUTURE_INDEX,params)

    #获取美元人民币汇率
    def exchange_rate(self):
        pass
        # EXCHANGE_RATE = "/api/v1/exchange_rate.do"
        # return httpGet(self.__url,EXCHANGE_RATE,'')

    #获取预估交割价
    def future_estimated_price(self,symbol):
        pass
        # FUTURE_ESTIMATED_PRICE = "/api/v1/future_estimated_price.do"
        # params=''
        # if symbol:
        #     params = 'symbol=' +symbol
        # return httpGet(self.__url,FUTURE_ESTIMATED_PRICE,params)

    #期货全仓账户信息
    def future_userinfo(self):
        pass
        # FUTURE_USERINFO = "/api/v1/future_userinfo.do?"
        # params ={}
        # params['api_key'] = self.__apikey
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_USERINFO,params)

    #期货全仓持仓信息
    def future_position(self,symbol,contractType):
        pass
        # FUTURE_POSITION = "/api/v1/future_position.do?"
        # params = {
        #     'api_key':self.__apikey,
        #     'symbol':symbol,
        #     'contract_type':contractType
        # }
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_POSITION,params)


    #期货批量下单
    def future_batchTrade(self,symbol,contractType,orders_data,leverRate):
        pass
        # FUTURE_BATCH_TRADE = "/api/v1/future_batch_trade.do?"
        # params = {
        #     'api_key':self.__apikey,
        #     'symbol':symbol,
        #     'contract_type':contractType,
        #     'orders_data':orders_data,
        #     'lever_rate':leverRate
        # }
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_BATCH_TRADE,params)

    

    #期货逐仓账户信息
    def future_userinfo_4fix(self):
        pass
        # FUTURE_INFO_4FIX = "/api/v1/future_userinfo_4fix.do?"
        # params = {'api_key':self.__apikey}
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_INFO_4FIX,params)

    #期货逐仓持仓信息
    def future_position_4fix(self,symbol,contractType,type1):
        pass
        # FUTURE_POSITION_4FIX = "/api/v1/future_position_4fix.do?"
        # params = {
        #     'api_key':self.__apikey,
        #     'symbol':symbol,
        #     'contract_type':contractType,
        #     'type':type1
        # }
        # params['sign'] = buildMySign(params,self.__secretkey)
        # return httpPost(self.__url,FUTURE_POSITION_4FIX,params)







    
