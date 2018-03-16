#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

import sys,commands
import os
import time

def getAllPyPid(dat):
    lines = dat.split('\n')
    tmpdic = {}
    for l in lines:
        tmpl = ' '.join(l.split())
        items = tmpl.split(' ')
        tmpdic[items[0]] = items
    return tmpdic

def isPIDHeave(pid):
    a,b = commands.getstatusoutput('/Users/mage/Documents/tool/cmdtool/pspy')
    dic = getAllPyPid(b)
    if pid in dic:
        print('进制运行正常:')
        print dic[pid]
        return True
    else:
        return False
def getNewPID(flogstr = '/Users/mage/Library/Python/3.6/bin/marketmaker'):
    a,b = commands.getstatusoutput('/Users/mage/Documents/tool/cmdtool/pspy')
    dic = getAllPyPid(b)
    for k in dic.keys():
        if flogstr in dic[k]:
            return k
    return None

def openTerminalWithNew(pcmd):
    cmd = "/usr/bin/osascript -e 'tell application \"Terminal\" to do script\"/bin/sh %s\"'"%(pcmd)
    print(cmd)
    os.system(cmd)
    time.sleep(30)
    npid = getNewPID()
    return npid

def sayWords(words):
    os.system('/usr/bin/say %s'%(words))

def main(pid,ptime,rerun = None):
    # a = os.system('/Users/mage/Documents/tool/cmdtool/pspy')
    print(rerun)

    tmppid = pid

    delaystart = 60   #进程延时重新启动时间
    rstarttimes = 0

    while True:
        if not isPIDHeave(tmppid):
            saywords = '进程%s已停止，注意查看'%(tmppid)
            sayWords(saywords)
            if rerun != None:
                rstarttimes += 1
                saywords = '新进程将在60秒后重新启动，本次启动为进程退出后第%d次重新启动'%(rstarttimes)
                sayWords(saywords)
                time.sleep(delaystart)
                print('rerun sh')
                npid = openTerminalWithNew(rerun)
                if npid != None:
                    tmppid = npid
                    saywords = '新进程启动成功,进程ID:%s'%(npid)
                    sayWords(saywords)
                else:
                    tmpdelay = rstarttimes*delaystart
                    saywords = '新进程启动失败,新进程将在%d秒之后再次启动'%(tmpdelay)
                    sayWords(saywords)
                    time.sleep(tmpdelay)
                    continue
        time.sleep(ptime)
if __name__=="__main__":  
    args = sys.argv
    if len(args) == 3:
        pid = args[1]     #邮件标题  
        psleeptime = args[2]
        main(pid,int(psleeptime))
    elif len(args) == 4:
        print(args)
        pid = args[1]     #邮件标题  
        psleeptime = args[2]
        rerunsh = args[3]
        main(pid,int(psleeptime),rerunsh)
    else:
        print "请输入要监控的python进制PID和检测时间间隔"

   
