#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time
import platform
import zlib

#http://www.cnblogs.com/freeliver54/archive/2008/04/08/1142356.html

#http://blog.csdn.net/xtx1990/article/details/7288903 

class SystemMsgObj(object):
    """docstring for SystemMsgObj"""
    def __init__(self):
        super(SystemMsgObj, self).__init__()
        self.sysversion = platform.version()
        self.sysplatform = platform.platform()
        self.sysSystem = platform.system()
        self.ver = ''
        self.ostype = 0        #1.windows,2.mac,3.linux
        if self.sysSystem == 'Windows':  #mac系统
            self.ostype = 1        #1.windows,2.mac,3.linux
            self.ver = platform.win32_ver()
        elif self.sysSystem == 'Darwin':
            self.ostype = 2
            self.ver = platform.mac_ver()
            
        elif self.sysSystem == 'Linux':
            self.ostype = 3
            self.ver = platform.linux_distribution()
        self.c = None
        self.sysMsg = {}
        self.sysMsg['osversion'] = str(self.sysversion)
        self.sysMsg['osplatform'] = str(self.sysplatform)
        self.sysMsg['os'] = str(self.sysSystem)
        self.sysMsg['ver'] = self.ver
        self.sysMsg['ostype'] = self.ostype
        if self.ostype == 1:
            import wmi
            self.c = wmi.WMI()
            self.initWinSystemHardMsg()
        elif self.ostype == 2:
            self.initMacSystemHardMsg()
        elif self.ostype == 3:
            self.initLinuxSystemHardMsg()

        self.getUserHardID()
    def initWinSystemHardMsg(self):
        self.sysMsg['cpu'] = self._printCPU()
        self.sysMsg['mainboard'] = self._printMain_board()
        self.sysMsg['BIOS'] = self._printBIOS()
        self.sysMsg['disk'] = self._printDisk()
        self.sysMsg['memory'] = self._printPhysicalMemory()
        self.sysMsg['battery'] = self._printBattery()
        self.sysMsg['MacAddr'] = self._printMacAddress()
        self.getUserHardID()
        return self.sysMsg
    def initMacSystemHardMsg(self):
        pass
    def initLinuxSystemHardMsg(self):
        pass

    def getSysMsg(self):
        return self.sysMsg

    def getUserHardID(self):
        if self.ostype == 1: #windwos
            self.sysMsg['userHardID'] = ''
            #windows下以电脑主板的UUID为编号
            #当主板UUID不存存或者无效时，使用容量最大硬盘的UUID + CPUID的MD5值
            #如果硬盘UUID无法获取，使用网卡MAC地址 + CPUID
        elif self.ostype == 2: #mac
            self.sysMsg['userHardID'] = ''

        elif self.ostype == 3: #linux

            self.sysMsg['userHardID'] = ''

    #处理器
    def _printCPU(self):
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        for cpu in self.c.Win32_Processor():     
            tmpdict["cpuid"] = cpu.ProcessorId.strip()
            tmpdict["CpuType"] = cpu.Name
            tmpdict['systemName'] = cpu.SystemName
            try:
                tmpdict["CpuCores"] = cpu.NumberOfCores
            except:
                tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed 
            tmpdict['DataWidth'] = cpu.DataWidth
        # print tmpdict
        return  tmpdict

    #主板
    def _printMain_board(self):
        boards = []
        # print len(c.Win32_BaseBoard()):
        for board_id in self.c.Win32_BaseBoard():
            tmpmsg = {}
            tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]   #主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
            tmpmsg['SerialNumber'] = board_id.SerialNumber                #主板序列号
            tmpmsg['Manufacturer'] = board_id.Manufacturer       #主板生产品牌厂家
            tmpmsg['Product'] = board_id.Product                 #主板型号
            boards.append(tmpmsg)
        print boards
        return boards

    #BIOS
    def _printBIOS(self):
        bioss = []
        for bios_id in self.c.Win32_BIOS():
            tmpmsg = {}
            tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics   #BIOS特征码
            tmpmsg['version'] = bios_id.Version                           #BIOS版本
            tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()                 #BIOS固件生产厂家
            tmpmsg['ReleaseDate'] = bios_id.ReleaseDate                   #BIOS释放日期
            tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion       #系统管理规范版本
            bioss.append(tmpmsg)
        print bioss
        return bioss

    #硬盘
    def _printDisk(self):
        disks = []
        for disk in self.c.Win32_DiskDrive():
            # print disk.__dict__
            tmpmsg = {}
            tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
            tmpmsg['DeviceID'] = disk.DeviceID
            tmpmsg['Caption'] = disk.Caption
            tmpmsg['Size'] = disk.Size
            tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
            disks.append(tmpmsg)
        for d in disks:
            print d
        return disks

    #内存
    def _printPhysicalMemory(self):
        memorys = []
        for mem in self.c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
            tmpmsg['BankLabel'] = mem.BankLabel
            tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
            tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
            tmpmsg['Capacity'] = mem.Capacity
            tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
            memorys.append(tmpmsg)
        for m in memorys:
            print m
        return memorys

    #电池信息，只有笔记本才会有电池选项
    def _printBattery(self):
        isBatterys = False
        for b in self.c.Win32_Battery():
            isBatterys = True
        return isBatterys

    #网卡mac地址：
    def _printMacAddress(self):
        macs = []
        for n in  self.c.Win32_NetworkAdapter():
            mactmp = n.MACAddress
            if mactmp and len(mactmp.strip()) > 5:
                tmpmsg = {}
                tmpmsg['MACAddress'] = n.MACAddress
                tmpmsg['Name'] = n.Name
                tmpmsg['DeviceID'] = n.DeviceID
                tmpmsg['AdapterType'] = n.AdapterType
                tmpmsg['Speed'] = n.Speed
                macs.append(tmpmsg)
        print macs
        return macs

def main():
    ostmp = SystemMsgObj()
    osmsg = ostmp.getSysMsg()
    print osmsg
if __name__ == '__main__':
    main()
