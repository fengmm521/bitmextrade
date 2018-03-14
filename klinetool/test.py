#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于访问OKCOIN 期货REST API


import time
import datetime
from magetool import timetool


def main():
    utc = "2018-03-14T13:40:00.000Z"
    # print(timetool.utcStrTimeToTime(utc))
    print(timetool.utcStrTimeToTime(utc))
    # datetime.datetime(2014, 9, 18, 10, 42, 16)

# def test():

#     dt = '2018-03-14T13:40:00.000Z'
#     timeArray = time.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")
#     print(timeArray)
#     timestamp = timetool.datetime2timestamp(timeArray)
#     print(timetool.datetime2timestamp(timeArray))
#     print(timetool.timestamp2datetime(timestamp))

#     timestamp = time.time()
#     timestruct = time.localtime(timestamp)
#     print(time.strftime('%Y-%m-%d %H:%M:%S', timestruct)) # 2016-12-22 10:49:57
#     time.utcfromtimestamp(timestamp)


if __name__ == '__main__':
    main()




    
