#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json


def saveListWithJson(datas,jsonpth):
    ostr = json.dumps(datas)
    f = open(jsonpth,'w')
    f.write(ostr)
    f.close()

def getListDataFromJsonFile(jpth):
    f = open(jpth,'r')
    jstr = f.read()
    f.close()
    datas = json.loads(jstr)
    return datas

def saveDicWithJson(dic,jsonpth):
    ostr = json.dumps(dic)
    f = open(jsonpth,'w')
    f.write(ostr)
    f.close()

def getDicDataFromJsonFile(jpth):
    f = open(jpth,'r')
    jstr = f.read()
    f.close()
    datas = json.loads(jstr)
    return datas

def saveListWithLineTxt(datas,txtpth):
    ostr = ''
    for d in datas:
        ostr += str(d) + '\n'
    ostr = ostr[:-1]
    f = open(txtpth,'w')
    f.write(ostr)
    f.close()

#获取多维数组中的某一维数据，组成一个新数组
def getMutlListWithIndex(datas,idx = 0):
    vtmp = [x[idx] for x in datas]
    return vtmp

def subList(lis1,lis2):
    v1 = list(lis1)
    v2 = list(lis2)
    v = list(map(lambda x: x[0]-x[1], zip(v1, v2)))
    return v

def getListWithCSVFile(csvpth,isHeaveHand = False):
    outs = []
    f = open(csvpth,'r')
    lines = f.readlines()
    f.close()
    if isHeaveHand:
        lines = lines[1:]

    for l in lines:
        tmpl = l.replace('\n','')
        tmpl = tmpl.replace('\r','')
        tmps = tmpl.split(',')
        if len(tmps) > 0:
            outs.append(tmps)
    return outs

if __name__ == '__main__':
    pass
    v1 = [2.4,3.3,4.2,8.1]
    v2 = [1,2,1,4]
    v = subList(v1, v2)
    print(v)
