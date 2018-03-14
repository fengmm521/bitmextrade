#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import chardet
import requests


def conventStrTOUtf8(oldstr):
    try:
        nstr = oldstr.encode("utf-8")
        return nstr
    except Exception as e:
        print('nstr do not encode utf-8')
    cnstrtype = chardet.detect(oldstr)['encoding']
    utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    return utf8str

def postDataToURL(purl,data):
    if purl[0:5] == 'https':
        response = requests.post(purl,data=data,verify=False)
        dat = response.text
        return dat
    else:
        response = requests.post(purl,data=data)
        dat = response.text
        return dat

def getUrl(purl):
    try:
        if purl[0:5] == 'https':
            res = requests.get(purl, verify=False)
            print(res.text)
            return res.text
        else:
            res = requests.get(purl)
            print(res.text)
            return res.text
    except Exception as e:
        print(e)
    return None

if __name__ == '__main__':
    pass