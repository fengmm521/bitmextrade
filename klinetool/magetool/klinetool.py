#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

def getAverageLineData(datas,pAver = 3,didx = 4):
    #[1517536380000,142.443,142.443,142,142,3486,244.8654307]
    ##时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
    outs = []
    for n in range(len(datas)):
        d = datas[n]
        tmps = [d[0]]
        if n < pAver -1:
            dtmp = datas[0:n+1]
            vtmp = [x[didx] for x in dtmp]
            mean = np.mean(vtmp)
            tmps.append(mean)
        else:
            dtmp = datas[n - pAver+1:n+1]
            vtmp = [x[didx] for x in dtmp]
            mean = np.mean(vtmp)
            tmps.append(mean)
        outs.append(tmps)
    return outs


if __name__ == '__main__':
    # print datetime.datetime.utcnow()
    # print timestamp_utc_now()
    # print timestamp2datetime(int(time.time()),True)
    tmpdat = '2017_7_17'
    print(getDateDaysFromOneDate(tmpdat))
    # outstr = timestamp2datetime(int(time.time() + 60 * 5),True)
    # print outstr